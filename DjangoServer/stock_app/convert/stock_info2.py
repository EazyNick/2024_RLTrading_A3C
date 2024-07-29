class DataParser:
    class StockInfo:
        def __init__(self, data):
            self.stock_code = data['pdno']
            self.stock_name = data['prdt_name']
            self.trade_type = data['trad_dvsn_name']
            self.holding_quantity = int(data['hldg_qty'])
            self.orderable_quantity = int(data['ord_psbl_qty'])
            self.purchase_avg_price = float(data['pchs_avg_pric'])
            self.purchase_amount = int(data['pchs_amt'])
            self.current_price = int(data['prpr'])
            self.evaluation_amount = int(data['evlu_amt'])
            self.evaluation_profit_loss_amount = int(data['evlu_pfls_amt'])
            self.evaluation_profit_loss_rate = float(data['evlu_pfls_rt'])
            self.fluctuation_rate = float(data['fltt_rt'])

    class AccountInfo:
        def __init__(self, data):
            self.total_cash_balance = int(data['dnca_tot_amt'])
            self.next_day_withdrawal_amount = int(data['nxdy_excc_amt'])
            self.previous_day_withdrawal_amount = int(data['prvs_rcdl_excc_amt'])
            self.securities_evaluation_amount = int(data['scts_evlu_amt'])
            self.total_evaluation_amount = int(data['tot_evlu_amt'])
            self.net_assets = int(data['nass_amt'])
            self.purchase_amount_sum = int(data['pchs_amt_smtl_amt'])
            self.evaluation_amount_sum = int(data['evlu_amt_smtl_amt'])
            self.evaluation_profit_loss_sum = int(data['evlu_pfls_smtl_amt'])
            self.total_assets_evaluation_previous_day = int(data['bfdy_tot_asst_evlu_amt'])
            self.assets_fluctuation_amount = int(data['asst_icdc_amt'])
            self.assets_fluctuation_rate = float(data['asst_icdc_erng_rt'])

    @classmethod
    def parse_account_data(cls, data):
        stock_info_list = [cls.StockInfo(stock) for stock in data['output1']]
        account_info = cls.AccountInfo(data['output2'][0])
        return stock_info_list, account_info


class AccountFormatter:
    @staticmethod
    def format(stocks, account):
        headers = [
            "상품번호", "      상품명      ", "보유수량", "  매입금액  ", "   현재가   ", 
            "평가손익율", "  평가손익  "
        ]
        
        print(f"예수금 : {account.total_cash_balance:,}원 평가금 : {account.total_evaluation_amount:,}원 손익 : {account.evaluation_profit_loss_sum:,}원")
        print("+" + "-"*100 + "+")
        print("| " + " | ".join(headers) + " |")
        print("+" + "-"*100 + "+")
        
        for stock in stocks:
            print("| {stock_code: <8} | {stock_name: <14} | {holding_quantity: <6}주 | {purchase_amount: >10,}원 | {current_price: >10,}원 | {evaluation_profit_loss_rate: >9.2f}% | {evaluation_profit_loss_amount: >10,}원 |".format(
                stock_code=stock.stock_code,
                stock_name=stock.stock_name,
                holding_quantity=stock.holding_quantity,
                purchase_amount=stock.purchase_amount,
                current_price=stock.current_price,
                evaluation_profit_loss_rate=stock.evaluation_profit_loss_rate,
                evaluation_profit_loss_amount=stock.evaluation_profit_loss_amount
            ))
        print("+" + "-"*100 + "+")


if __name__ == "__main__":
    data = {
        'ctx_area_fk100': ' ',
        'ctx_area_nk100': ' ',
        'output1': [
            {
                'pdno': '005930',
                'prdt_name': '삼성전자',
                'trad_dvsn_name': '현금',
                'bfdy_buy_qty': '0',
                'bfdy_sll_qty': '0',
                'thdt_buyqty': '0',
                'thdt_sll_qty': '0',
                'hldg_qty': '2',
                'ord_psbl_qty': '2',
                'pchs_avg_pric': '80750.0000',
                'pchs_amt': '161500',
                'prpr': '87100',
                'evlu_amt': '174200',
                'evlu_pfls_amt': '12700',
                'evlu_pfls_rt': '7.86',
                'evlu_erng_rt': '7.86377709',
                'loan_dt': '',
                'loan_amt': '0',
                'stln_slng_chgs': '0',
                'expd_dt': '',
                'fltt_rt': '2.96000000',
                'bfdy_cprs_icdc': '2500',
                'item_mgna_rt_name': '20%',
                'grta_rt_name': '',
                'sbst_pric': '0',
                'stck_loan_unpr': '0.0000'
            }
        ],
        'output2': [
            {
                'dnca_tot_amt': '9838480',
                'nxdy_excc_amt': '9838480',
                'prvs_rcdl_excc_amt': '9838480',
                'cma_evlu_amt': '0',
                'bfdy_buy_amt': '0',
                'thdt_buy_amt': '0',
                'nxdy_auto_rdpt_amt': '0',
                'bfdy_sll_amt': '0',
                'thdt_sll_amt': '0',
                'd2_auto_rdpt_amt': '0',
                'bfdy_tlex_amt': '0',
                'thdt_tlex_amt': '0',
                'tot_loan_amt': '0',
                'scts_evlu_amt': '174200',
                'tot_evlu_amt': '10012680',
                'nass_amt': '10012680',
                'fncg_gld_auto_rdpt_yn': '',
                'pchs_amt_smtl_amt': '161500',
                'evlu_amt_smtl_amt': '174200',
                'evlu_pfls_smtl_amt': '12700',
                'tot_stln_slng_chgs': '0',
                'bfdy_tot_asst_evlu_amt': '10007680',
                'asst_icdc_amt': '5000',
                'asst_icdc_erng_rt': '0.04996163'
            }
        ],
        'rt_cd': '0',
        'msg_cd': '20310000',
        'msg1': '모의투자 조회가 완료되었습니다.'
    }

    stock_info_list, account_info = DataParser.parse_account_data(data)

    formatter = AccountFormatter()
    formatter.format(stock_info_list, account_info)