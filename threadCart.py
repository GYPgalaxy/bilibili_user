import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go

fh = pd.read_csv('./poj_file/runtime_avg.csv', encoding='utf-8')


def drawThreadCart():
    thread_num_list = fh.threadNum.tolist()
    craw_time_list = fh.subTimeAvg.tolist()
    accuracy_list = fh.accuracy.tolist()
    # data = go.Scatter(
    #     x=thread_num_list,
    #     y=craw_time_list,
    # )
    mlayout = dict(title='不同线程数运行效率',
                   xaxis=dict(title='线程数（个）'),  # 横轴坐标
                   yaxis=dict(title='运行时间（秒）'),  # 纵轴坐标
                   )
    #
    # fig = dict(data=data, layout=mlayout)
    # plot(fig, filename='threadCart.html')
    trace1 = go.Scatter(
        x=thread_num_list,
        y=craw_time_list
    )
    # trace2 = go.Scatter(
    #     x=thread_num_list,
    #     y=accuracy_list
    # )
    fig1 = dict(data=trace1, layout=mlayout)
    # fig2 = dict(data=trace2, layout=mlayout)

    plot(fig1, filename='threadCart.html')
    # plot(fig2, filename='threadCart.html')


if __name__ == '__main__':
    drawThreadCart()
    print('end')
