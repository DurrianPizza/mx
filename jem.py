import streamlit as st
import pandas as pd

def calculate_gem_cost(target_level, level1_price, synthesis_costs):
    """
    计算宝石合成成本
    :param target_level: 目标等级
    :param level1_price: 1级宝石价格（梦幻币）
    :param synthesis_costs: 各级合成费用列表
    :return: (总费用, 宝石费用, 合成费用, 各级宝石数量)
    """
    # 初始化各级宝石需求数量
    gem_counts = {i: 0 for i in range(1, target_level + 1)}
    
    # 递归计算所需1级宝石数量
    def calculate_required_gems(level):
        if level == 1:
            return 1
        return 2 * calculate_required_gems(level - 1)
    
    total_level1_needed = calculate_required_gems(target_level)
    gem_counts[1] = total_level1_needed
    
    # 计算宝石费用
    gem_cost = total_level1_needed * level1_price
    
    # 计算合成费用
    synthesis_cost = 0
    for level in range(1, target_level):
        if level - 1 < len(synthesis_costs):
            # 合成次数 = 需要的当前等级宝石数 / 2
            syntheses_needed = gem_counts[1] // (2 ** (level - 1)) // 2
            synthesis_cost += syntheses_needed * synthesis_costs[level - 1]
    
    total_cost = gem_cost + synthesis_cost
    return total_cost, gem_cost, synthesis_cost, gem_counts

def main():
    st.title("💎 宝石合成计算器")
    
    # 输入参数
    col1, col2 = st.columns(2)
    
    with col1:
        target_level = st.number_input(
            "目标宝石等级", 
            min_value=1, 
            max_value=20, 
            value=5
        )
        
        level1_price = st.number_input(
            "1级宝石单价（梦幻币）", 
            min_value=0, 
            value=10000
        )
    
    with col2:
        st.write("合成费用（梦幻币）")
        synthesis_costs = []
        cols = st.columns(2)
        
        for i in range(target_level - 1):
            with cols[i % 2]:
                cost = st.number_input(
                    f"{i+1}→{i+2}级",
                    min_value=0,
                    value=0,
                    key=f"syn_cost_{i}"
                )
                synthesis_costs.append(cost)
    
    # 计算按钮
    if st.button("计算"):
        total_cost, gem_cost, synthesis_cost, gem_counts = calculate_gem_cost(target_level, level1_price, synthesis_costs)
        
        # 显示结果
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("宝石费用", f"{gem_cost:,} 梦幻币")
        
        with col2:
            st.metric("合成费用", f"{synthesis_cost:,} 梦幻币")
        
        with col3:
            st.metric("总费用", f"{total_cost:,} 梦幻币")
        
        # 详细分解
        st.write("### 合成详情")
        
        data = []
        for level in range(1, target_level + 1):
            data.append({
                '宝石等级': f"{level}级",
                '所需数量': f"{gem_counts[1] // (2 ** (level - 1)):,} 颗"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
