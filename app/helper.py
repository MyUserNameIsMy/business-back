import numpy as np
import pandas as pd
import numpy_financial as npf


def convert_columns(df):
    new_columns = []
    for col in df.columns:
        try:
            new_columns.append(int(col))
        except ValueError:
            new_columns.append(col)
    return new_columns


def calculate_pv(_cash_flow, _cost_of_capital):
    flow = {}
    for idx, value in _cash_flow.items():
        if idx == 'Year' or int(idx) == 0:
            flow[idx] = value
            continue
        flow[idx] = value / pow(1 + _cost_of_capital, idx)
    return pd.Series(flow)


def analyze_business(filename):
    df_initial = pd.read_excel(filename, sheet_name="initial", index_col=0)
    df_inflow = pd.read_excel(filename, sheet_name="inflow", index_col=0)
    df_outflow = pd.read_excel(filename, sheet_name="outflow", index_col=0)

    rate = df_initial['value'][0]
    investment = df_initial['value'][1]

    df_inflow.columns = convert_columns(df_inflow)
    filter_in_col = [col for col in list(df_inflow) if type(col) == int and col > 0]

    df_outflow.columns = convert_columns(df_outflow)
    filter_out_col = [col for col in list(df_outflow) if type(col) == int and col > 0]

    # cash inflow and cash outflow
    df_inflow.loc['Cash Inflow'] = df_inflow[filter_in_col].sum(numeric_only=True, axis=0)
    df_outflow.loc['Cash Outflow'] = df_outflow[filter_out_col].sum(numeric_only=True, axis=0)

    # PV of cash inflow and PV of cash outflow
    df_inflow.loc['PV of Cash Inflow'] = calculate_pv(df_inflow.loc['Cash Inflow'], rate)
    df_outflow.loc['PV of Cash Outflow'] = calculate_pv(df_outflow.loc['Cash Outflow'], rate)
    df_outflow[0]['PV of Cash Outflow'] = investment

    # cash flow
    cash_flow = df_inflow[filter_in_col].loc['Cash Inflow'] - df_outflow[filter_out_col].loc['Cash Outflow']

    # NPV
    npv = npf.npv(rate, cash_flow.values)
    # IRR
    cash_flow_list = cash_flow.values.tolist()
    cash_flow_list.insert(0, -investment)
    irr = npf.irr(cash_flow_list)
    #PI
    pv_sum = sum(df_inflow[filter_in_col].loc['PV of Cash Inflow'].values.tolist())
    pi = pv_sum/investment
    #pbpd
    avg_cash_flow = np.average(cash_flow)
    pbpd = investment/avg_cash_flow

    return {'npv': npv-investment, 'irr': np.round(irr*100, 1), 'pi': np.round(pi, 1), 'pbpd': np.round(pbpd, 2)}