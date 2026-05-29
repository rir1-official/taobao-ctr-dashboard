import pandas as pd
import os
import streamlit as st


class DataLoader:
    @staticmethod
    @st.cache_data
    def load_data(file_name, source='raw'):
        """
        加载数据的通用工具函数
        source: 'raw' or 'processed'
        """
        # 获取当前文件所在的目录的上一级目录（即项目根目录）
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data', source, file_name)

        if not os.path.exists(file_path):
            st.error(f"文件不存在: {file_path}")
            return None

        try:
            # 读取CSV，处理可能的编码问题
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"读取文件失败: {e}")
            return None