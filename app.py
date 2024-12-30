import streamlit as st  # 导入Streamlit库，并简写为st，用于构建Web应用。
import requests  # 导入requests库，用于发送HTTP请求。
import jieba  # 导入jieba库，用于中文分词。
from collections import Counter  # 从collections库中导入Counter类，用于统计词频。
from pyecharts.charts import WordCloud  # 从pyecharts库中导入WordCloud类，用于生成词云图。
from pyecharts import options as opts  # 从pyecharts库中导入options模块，并简写为opts，用于配置图表。
from streamlit.components.v1 import html  # 从streamlit.components.v1库中导入html函数，用于在Streamlit应用中显示HTML内容。
import plotly.express as px  # 导入plotly.express库，并简写为px，用于创建交互式图表。
import pandas as pd  # 导入pandas库，并简写为pd，用于数据处理。

# 设计文本输入框，用户输入文章URL
url = st.text_input("请输入文章URL")  # 创建一个文本输入框，让用户输入文章的URL。

# 请求URL抓取文本内容
if url:  # 如果用户输入了URL，
    try:  # 尝试执行以下代码，
        response = requests.get(url)  # 发送GET请求到指定的URL。
        response.raise_for_status()  # 如果请求失败，抛出异常。
        text = response.text  # 获取响应的文本内容。

        # 对文本分词，统计词频
        words = jieba.cut(text)  # 使用jieba对文本进行分词。
        word_counts = Counter(words)  # 使用Counter统计词频。

        # 交互过滤低频词
        min_freq = st.sidebar.slider("最小词频", 1, 100, 10)  # 在侧边栏创建一个滑块，让用户选择最小词频。

        # 过滤低频词
        filtered_words = {word: count for word, count in word_counts.items() if count >= min_freq}  # 过滤掉词频小于用户设定值的词。
        filtered_words = Counter(filtered_words)  # 将过滤后的词频转换回Counter对象。

        # 展示词频排名前20的词汇
        top_words = filtered_words.most_common(20)  # 获取词频排名前20的词汇。
        st.write("词频排名前20的词汇:")  # 显示标题。
        st.write(top_words)  # 显示排名前20的词汇。

        # 使用pyecharts绘制词云
        wordcloud = WordCloud()  # 创建一个WordCloud对象。
        wordcloud.add("", list(filtered_words.items()), word_size_range=[20, 100])  # 向词云中添加数据，并设置字体大小范围。
        wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="词云图"))  # 设置词云图的全局配置，如标题。
        wordcloud_html = wordcloud.render_embed()  # 将词云图渲染为HTML。
        html(wordcloud_html, height=600)  # 在Streamlit应用中显示词云图。

        # 构建 streamlit的st.sidebar进行图型筛选
        chart_type = st.sidebar.selectbox("选择图表类型", ["柱状图", "饼图", "线图", "散点图", "面积图", "箱型图", "K线图"])  # 在侧边栏创建一个下拉框，让用户选择图表类型。

        # 根据选择的图表类型绘制图表
        if chart_type == "柱状图":
            st.bar_chart([(word, count) for word, count in top_words])  # 如果选择柱状图，使用Streamlit的bar_chart函数显示词频数据。
        elif chart_type == "饼图":
            fig = px.pie(values=[count for word, count in top_words], names=[word for word, count in top_words], title="词频饼图")  # 如果选择饼图，使用Plotly Express创建饼图。
            st.plotly_chart(fig)  # 在Streamlit应用中显示饼图。
        elif chart_type == "线图":
            df = pd.DataFrame(top_words, columns=['Word', 'Count'])  # 如果选择线图，将数据转换为DataFrame。
            fig = px.line(df, x='Word', y='Count', title="词频趋势图")  # 使用Plotly Express创建线图。
            st.plotly_chart(fig)  # 显示线图。
        elif chart_type == "散点图":
            df = pd.DataFrame(top_words, columns=['Word', 'Count'])  # 如果选择散点图，将数据转换为DataFrame。
            fig = px.scatter(df, x='Word', y='Count', title="词频散点图")  # 使用Plotly Express创建散点图。
            st.plotly_chart(fig)  # 显示散点图。
        elif chart_type == "面积图":
            df = pd.DataFrame(top_words, columns=['Word', 'Count'])  # 如果选择面积图，将数据转换为DataFrame。
            fig = px.area(df, x='Word', y='Count', title="词频面积图")  # 使用Plotly Express创建面积图。
            st.plotly_chart(fig)  # 显示面积图。
        elif chart_type == "箱型图":
            df = pd.DataFrame(top_words, columns=['Word', 'Count'])  # 如果选择箱型图，将数据转换为DataFrame。
            fig = px.box(df, x='Word', y='Count', title="词频箱型图")  # 使用Plotly Express创建箱型图。
            st.plotly_chart(fig)  # 显示箱型图。
        elif chart_type == "K线图":
            df = pd.DataFrame(top_words, columns=['Word', 'Count'])  # 如果选择K线图，将数据转换为DataFrame。
            fig = px.line(df, x='Word', y='Count', title="词频K线图")  # 使用Plotly Express创建折线图作为K线图的替代。
            st.plotly_chart(fig)  # 显示K线图。

    except requests.RequestException as e:  # 如果请求过程中发生异常，
        st.error(f"请求错误: {e}")  # 在Streamlit应用中显示错误信息。
    except Exception as e:  # 如果发生其他异常，
        st.error(f"发生错误: {e}")  # 在Streamlit应用中显示错误信息。