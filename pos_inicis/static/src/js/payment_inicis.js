odoo.define('pos_inicis.payment', function (require) {
"use strict";

var core = require('web.core');
var PaymentInterface = require('point_of_sale.PaymentInterface');
const { Gui } = require('point_of_sale.Gui');

var _t = core._t;

const transactionCode = {
    Approve: {
        card: "S0",
        unionpay: "E0",
        cash_receipts: "41",
        appcard: "P0",
        lpay: "L0",
        kakaopay: "K0",
        alipay: "A0",
        zeropay: "Z0",
        bcqr: "Q0",
        naverpay: "N0",
    },
    Reversal: {
        card: "S1",
        unionpay: "E1",
        cash_receipts: "42",
        appcard: "P1",
        lpay: "L1",
        kakaopay: "K1",
        alipay: "A1",
        zeropay: "Z1",
        bcqr: "Q1",
        naverpay: "N1",
    }
};

const transactionType = {
    Approve: "0210",
    Reversal: "0430",
};

const responseCode = {
    '0000': "정상 처리",
    '1111': "모빌리언스 카드 인증 응답",
    '4001': "리더기 포트 미설정",
    '4002': "무결성점검 실패",
    '4003': "요청한 TID와 저장된 TID가 다름",
    '4004': "IC 리더기 포트를 열기 실패",
    '4005': "IC 리더기 시리얼 번호가 불일치",
    '4006': "승인 서버IP 형식이 맞지 않음",
    '4007': "승인 서버 포트 미설정",
    '4008': "IC or RF 리더기 연결 확인 요망",
    '4009': "정의되지 않은 거래 요청",
    '5001': "IC 카드 읽기 실패",
    '5002': "거래에 필요한 금액이 없음",
    '5003': "IC 카드 인식이 불가능",
    '5004': "IC 카드가 삽입되어 있음",
    '5005': "거래flow에서 상황에 맞지 않는 명령이 호출",
    '5006': "IC 카드인데 MS 리딩이 발생",
    '5007': "IC 카드처리 중 강제로 카드 분리",
    '5008': "기타 오류",
    '5009': "기타 오류(정의되지 않은 오류)",
    '5010': "은련카드를 일반 거래 요청",
    '5011': "리더기가 카드 구분(IC,MS) 판단하지 못함",
    '5012': "pin 미입력",
    '5013': "리더기 연결이 끊어짐",
    '5014': "리더기 사용 불가",
    '5015': "리더기 명령 기타 응답",
    '5016': "은련카드 AID 선택 오류",
    '5017': "현금영수증 고객 정보 미입력",
    '5018': "App 카드 길이 오류",
    '5019': "전문 파싱 에러 (emvlen or pinlen 길이가 비정상 데이터일 경우)",
    '5020': "핀패드 설정이 안되어 있으면 은련카드 거래 안됨",
    '5021': "서명/PIN패드 연결 실패",
    '5022': "PIN설정 실패",
    '6001': "IC카드를 비정상적으로 삽입했을 경우",
    '7001': "DLL 파일이 없음",
    '7002': "DLL 명령어가 없음",
    '7003': "pin 암호화 오류",
    '8001': "거래중 사용자 중단 요청",
    '8002': "거래중 망취소 (리더기 판단)",
    '8003': "거래중 망취소 (응답 미수신)",
    '8004': "거래 거절 (승인 서버 기타 응답)",
    '8005': "pin 거래 MS 불가",
    '8006': "서명 오류 취소 (화면 서명 - 전송할 서명 파일 없음)",
    '8007': "카드 삽입 시간 초과",
    '8008': "사용자 취소",
    '8009': "barcode or QRcode 값 미입력",
    '8324': "거래 거절 (승인 서버 응답)",
    '8325': "거래 거절 (이미 취소된 취소 요청 거절 승인 서버 응답)",
    '8555': "거래 거절 (승인 서버 응답이 공백)",
    '8899': "거래 거절 (승인 서버 응답이 기타)",
    '8999': "망상-취소 처리 완료. 거래 확인 요망",
    '9997': "응답코드+기타오류 (서버수신전문에 응답코드는 있는데 응답메시지가 " +
        "없는 경우 수신받은 응답코드 + 기타오류 set)(ex 7017 기타오류)",
    '9998': "서버 응답 메세지 그대로 (서버 수신전문에 응답코드는 Space인데 응답메세지가 있는 경우 응답코드 set)",
    '9999': "기타오류 (서버 수신 전문에 응답코드, 응답메세지가 Space인 경우 set)"
};

var PaymentInicis = PaymentInterface.extend({

    init: function () {
        this._super.apply(this, arguments);
        this.enable_reversals();
    },

    send_payment_request: function (cid) {
        this._super.apply(this, arguments);
        var type = this.pos.get_order().selected_paymentline.get_amount() > 0
            ? 'Approve' : 'Reversal';
        return this._sendTransaction(type);
    },

    send_payment_cancel: function (order, cid) {
        this._super.apply(this, arguments);
        return Promise.resolve();
    },
    
    send_payment_reversal: function (cid) {
        this._super.apply(this, arguments);
        return this._sendTransaction('Reversal');
    },

    pending_inicis_line: function() {
      return this.pos.get_order().paymentlines.find(
        paymentLine => paymentLine.payment_method.use_payment_terminal === 'inicis' && (!paymentLine.is_done()));
    },

    // private methods
    _get_tcode: function (type) {
        return transactionCode[type][this.payment_method.inicis_tcode];
    },

    _get_tid: function () {
        return this.payment_method.inicis_tid;
    },

    _get_trantype: function (type) {
        return transactionType[type];
    },

    _get_error_message: function (code) {
        return responseCode[code];
    },

    _sendTransaction: function (type) {
        var self = this;
        return new Promise(function (resolve, reject) {
            console.log("connecting to WebSocket");
            self.ws = new WebSocket("ws://localhost:9001");//("ws://localhost:9419/WebSocketEx/websocket");
            self.ws.addEventListener('open', self._onOpen.bind(self, resolve, type));
            self.ws.addEventListener('message', self._onMessage.bind(self, resolve, type));
            self.ws.addEventListener('close', self._onClose.bind(self));
            self.ws.addEventListener('error', self._onError.bind(self, reject));
        }).then(function (value) {
            console.log('value = ', value);
            return Promise.resolve(value);
        }).catch(function() {
            var line = self.pending_inicis_line();
            if (line) {
                line.set_payment_status('retry');
            }
            self._show_error(_t('The connection to your payment terminal failed.'));
            return Promise.resolve(false);
        }).finally(function(){
            if (self.ws) {
                self.ws.close();
            }
            var line = self.pending_inicis_line();
            console.log('transaction_id: ' + line.get_transaction_id());
        });
    },

    _onOpen: function (resolve, type, ev) {
        console.log('ws connected');
        console.log('type', type);
        console.log('ev', ev);
        if (this.ws.readyState === WebSocket.OPEN) {
            var data = this._inicis_data(type)
            console.log(data);
            this.ws.send(data);
            var line = this.pending_inicis_line();
            if (line) {
                console.log("waitingCard...");
                line.set_payment_status('waitingCard');
            }
        }
    },

    _onMessage: function (resolve, type, ev) {
        var data = ev.data;
        var param = {}
        var param_length = {
            trantype: 4,
            errcode: 4,
            cardno: 18,
            halbu: 2,
            tamt: 9,
            trandate: 6,
            trantime: 6,
            authno: 12,
            merno: 15,
            tran_serial: 12,
            stlinst: 30,
            reqinst: 30,
            signpath: 50,
            msg1: 100,
            msg2: 100,
            msg3: 100,
            msg4: 100,
            filler: 2+2+9+9+9+2+5+12+2+2+20+1+27,
            pgdata: 329
        };
        var from = 0;
        for (var key in param_length) {
            param[key] = data.substring(from, from+param_length[key]);
            from += param_length[key]
        }
        console.log(param);
        if (param['trantype'] === this._get_trantype(type)) {
            var order = this.pos.get_order();
            var line = order.selected_paymentline;
            line.set_transaction_id(param['authno'].trim());
            resolve(true);
        } else {
            this._show_error(_t(this._get_error_message(param['errcode'])));
            resolve(false);
        }
    },

    _onClose: function (ev) {
        console.log("Connection is closed...");
    },

    _onError: function (reject, ev) {
        reject();
        console.log("Transport error: " + ev);
    },

    _inicis_data: function (type) {
        var order = this.pos.get_order();
        var line = order.selected_paymentline;

        // 거래 구분
        var tcode = this._get_tcode(type);
        // 단말기 번호 : TID
        var tid = this._get_tid();
        // 할부 : 할부 개월 수 2자리 고정
        var halbu = this._padl(line.monthly_installment, 2, '0');
        // 결제금액 : 9자리
        var tamt = this._padl(Math.abs(line.amount), 9, '0');

        if( type == 'Approve' ) {
            //승인시 원거래일자 : 스페이스 6자리 , 원거래승인번호 : 스페이스 12자리
            var ori_date = "      ";
            var ori_authno = "            ";
            //미사용공백
            var flag= " ";
        }
        else if( type == 'Reversal' ) {
            var ori_date = moment(order.creation_date).format('YYMMDD');
            var ori_authno = this._padr(line.transaction_id, 12, ' ');
            var flag= "N";
        }

        // 거래고유번호 : 숫자앞에 0으로 채워서 6자리 + 공백 6자리
        let today = new Date();
        let Hours = today.getHours();
        let Minutes = today.getMinutes();
        let date = today.getDate();
        var tran_serial = this._padl(Hours,2,'0')+''+this._padl(Minutes,2,'0')+''+this._padl(date,2,'0');
        tran_serial = this._padr(tran_serial,12,' ');
        // 현금/수표조회 식별번호 : 스페이스(33자리)
        var idno = "                                 ";
        //다중TID사용여부
        var mTID = "0";
        //직전사인사용여부
        var Sign = "0";
        // 세금
        var tax_amt = this._padl('0', 9, '0');
        // 봉사료
        var sfee_amt = this._padl('0', 9, '0');
        // 비과세
        var free_amt = this._padl('0', 9, '0');
        // 컵보증금
        var cup_deposit = this._padl('0', 8, '0');
        //PG구분값
        var partner = order.get_partner();
        var orderline = order.selected_orderline;
        var orderno = this._padr(order.uid,64,' ');
        var ordername = this._padr(partner ? partner.name : '',27,' '); //한글인 경우 길이 2바이트 처리 예: 홍길동(6바이트)나머지 24바이트를 스페이스로 채움
        var orderproduct = this._padr(orderline ? orderline.get_full_product_name() : '',80,' ');
        var orderphone = this._padr(partner ? partner.phone : '',40,' ');
        var ordermail = this._padr(partner ? partner.email : '',60,' ');
        var ordermid = "1234567891";

        //var pgdata = "OFFPG"+orderno+ordername+orderproduct+orderphone+ordermail+ordermid;
        var pgdata = this._padl(' ', 289, ' ');

        //요청 전문
        var data = tcode+halbu+tamt+ori_date+ori_authno
					+tran_serial+idno+mTID+Sign+flag+tax_amt+sfee_amt+free_amt+tid+pgdata+cup_deposit;

        return data;
    },

    _show_error: function (msg, title) {
        if (!title) {
            title =  _t('Inicis Error');
        }
        Gui.showPopup('ErrorPopup',{
            'title': title,
            'body': msg,
        });
    },

    //문자열 오른쪽에 문자 채우기
    _padl: function (n, width, c) {
        n = n + '';
        return n.length >= width ? n : new Array(width - n.length + 1).join(c) + n;
    },

    //문자열 왼쪽에 문자 채우기
    _padr: function (n, width, c) {
        n = n + '';
        return n.length >= width ? n : n + new Array(width - n.length + 1).join(c);
    },
});

return PaymentInicis;
});
