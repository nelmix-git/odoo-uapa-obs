openerp.pos_payment = function (instance) {
    var module = instance.point_of_sale;
    var _t = instance.web._t;


    // Extend Model

    module.Paymentline = module.Paymentline.extend({
        initialize: function (attributes, options) {
            this._super('initialize', attributes, options);
            this.has_bank_name = this.cashregister.journal.has_bank_name;
            this.bank_name = false;
            this.has_cheque_number = this.cashregister.journal.has_cheque_number;
            this.cheque_number = false;
            this.has_cc_number = this.cashregister.journal.has_cc_number;
            this.cc_number = false;
            this.has_ba_number = this.cashregister.journal.has_ba_number;
            this.ba_number = false;
            this.has_trn_number = this.cashregister.journal.has_trn_number;
            this.trn_number = false;
        },
        set_bank_name: function(name) {
            if(this.has_bank_name){
                this.bank_name = name;
            }
        },
        set_check_number: function(number){
            if(this.has_cheque_number){
                this.cheque_number = number;
            }
        },
        
        set_cc_number: function(number1){
           if(this.has_cc_number){
                this.cc_number = number1;
            }
       },
        
       set_ba_number: function(number2){
            if(this.has_ba_number){
                this.ba_number = number2;
            }
        },
        
        set_trn_number: function(number3){
            if(this.has_trn_number){
                this.trn_number = number3;
            }
        },
        
        export_as_JSON: function(){
            obj = this._super('export_as_JSON');
            return _.extend(obj, {
                bank_name: this.bank_name,
                cheque_number: this.cheque_number,
                cc_number: this.cc_number,
                ba_number: this.ba_number,
                trn_number: this.trn_number,
            });
        },

    });

    // Extend Screen (payment line)
    module.PaymentScreenWidget = module.PaymentScreenWidget.extend({
        render_paymentline: function(line){
            node = this._super.apply(this, arguments);
            var el_fields  = openerp.qweb.render('Paymentline_Fields',{line: line}),
                el_fields  = _.str.trim(el_fields);
            var $container_div = $('<div>');
            $(node).appendTo($container_div);
            $(el_fields).appendTo($container_div);
            var el_node = $container_div.get(0);
            var bank_name = el_node.querySelector('.bank-name');
            if (bank_name){
                bank_name.line = line;
                bank_name.addEventListener('keyup', this.bank_name_change);
            }
            var check_number = el_node.querySelector('.check-number');
            if (check_number){
                check_number.line = line;
                check_number.addEventListener('keyup', this.check_number_change);
            }
            var cc_number = el_node.querySelector('.cc-number');
            if (cc_number){
                cc_number.line = line;
                cc_number.addEventListener('keyup', this.cc_number_change);
           }
            
            var ba_number = el_node.querySelector('.ba-number');
           if (ba_number){
                ba_number.line = line;
                ba_number.addEventListener('keyup', this.ba_number_change);
           }
            
            var trn_number = el_node.querySelector('.trn-number');
            if (trn_number){
               trn_number.line = line;
                trn_number.addEventListener('keyup', this.trn_number_change);
            }
            
            // el_node.line = line;
            line.node = el_node;
            return el_node;
        },

        bank_name_change: function(event){
            node = this;
            node.line.set_bank_name(this.value);
        },

        check_number_change: function(){
            node = this;
            node.line.set_check_number(this.value);
        },
        
        cc_number_change: function(){
            node = this;
            node.line.set_cc_number(this.value);
        },
        
        ba_number_change: function(){
            node = this;
           node.line.set_ba_number(this.value);
        },
        
          trn_number_change: function(){
            node = this;
            node.line.set_trn_number(this.value);
        },
        
        // Add fiscal position in summary info
        update_payment_summary: function () {
            res = this._super.apply(this, arguments);
            var currentOrder = this.pos.get('selectedOrder');
            var client = currentOrder.get_client();
            if (client && client.property_account_position){
                var $fiscal_info = this.$('.fiscal-position-info').show();
                $fiscal_info.find('.fiscal-position').html(client.property_account_position[1]);
            }
            return res;
        }
    });
};
