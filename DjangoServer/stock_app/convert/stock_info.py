# stock_info

def parse_account_data(data):
    # Output1
    output1 = data['output1'][0]
    stock_info = {
        'stock_code': output1['pdno'],
        'stock_name': output1['prdt_name'],
        'trade_type': output1['trad_dvsn_name'],
        'holding_quantity': int(output1['hldg_qty']),
        'orderable_quantity': int(output1['ord_psbl_qty']),
        'purchase_avg_price': float(output1['pchs_avg_pric']),
        'purchase_amount': int(output1['pchs_amt']),
        'current_price': int(output1['prpr']),
        'evaluation_amount': int(output1['evlu_amt']),
        'evaluation_profit_loss_amount': int(output1['evlu_pfls_amt']),
        'evaluation_profit_loss_rate': float(output1['evlu_pfls_rt']),
        'fluctuation_rate': float(output1['fltt_rt'])
    }

    # Output2
    output2 = data['output2'][0]
    account_info = {
        'total_cash_balance': int(output2['dnca_tot_amt']),
        'next_day_withdrawal_amount': int(output2['nxdy_excc_amt']),
        'previous_day_withdrawal_amount': int(output2['prvs_rcdl_excc_amt']),
        'securities_evaluation_amount': int(output2['scts_evlu_amt']),
        'total_evaluation_amount': int(output2['tot_evlu_amt']),
        'net_assets': int(output2['nass_amt']),
        'purchase_amount_sum': int(output2['pchs_amt_smtl_amt']),
        'evaluation_amount_sum': int(output2['evlu_amt_smtl_amt']),
        'evaluation_profit_loss_sum': int(output2['evlu_pfls_smtl_amt']),
        'total_assets_evaluation_previous_day': int(output2['bfdy_tot_asst_evlu_amt']),
        'assets_fluctuation_amount': int(output2['asst_icdc_amt']),
        'assets_fluctuation_rate': float(output2['asst_icdc_erng_rt'])
    }

    return stock_info, account_info
