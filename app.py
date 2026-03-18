import streamlit as st
import os
import subprocess
import shutil

# 页面配置
st.set_page_config(
    page_title="贪食蛇游戏 🐍",
    page_icon="🐍",
    layout="wide"
)

# 页面标题和说明
st.title("🐍 经典贪食蛇游戏")
st.subheader("基于 Python + Pygame + Streamlit 网页版")
st.markdown("""
### 🎮 游戏操作说明：
- **方向键**：控制蛇的移动方向（上/下/左/右）
- **C键**：游戏结束后重新开始
- **Q键**：退出游戏
- **目标**：吃到红色食物增长身体，避免撞墙/撞自身
""")

# 清理旧构建文件（避免缓存问题）
def clean_old_build():
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("web"):
        shutil.rmtree("web")

# 构建并运行游戏
def run_snake_game():
    try:
        # 清理旧文件
        clean_old_build()
        
        st.info("正在构建游戏...（首次运行可能需要10-20秒）")
        
        # 使用pygbag构建网页版游戏
        build_cmd = [
            "python", "-m", "pygbag",
            "--build",
            "--html",
            "snake_game.py"
        ]
        
        # 执行构建命令
        result = subprocess.run(
            build_cmd,
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
            timeout=120  # 超时时间2分钟
        )
        
        if result.returncode == 0:
            # 构建成功，显示游戏
            st.success("✅ 游戏构建完成！点击游戏窗口开始操作")
            
            # 游戏HTML文件路径
            game_html_path = os.path.join("build", "web", "snake_game.html")
            
            # 嵌入游戏到Streamlit页面
            st.markdown(f"""
            <iframe 
                src="{game_html_path}" 
                width="650" 
                height="650" 
                frameborder="0" 
                allowfullscreen
                style="border: 3px solid #4CAF50; border-radius: 10px; margin: 0 auto; display: block;"
            >
            </iframe>
            """, unsafe_allow_html=True)
        else:
            # 构建失败，显示错误信息
            st.error(f"❌ 游戏构建失败：{result.stderr}")
            st.code(result.stdout)
    
    except subprocess.TimeoutExpired:
        st.error("❌ 构建超时！请检查网络或重试")
    except Exception as e:
        st.error(f"❌ 运行出错：{str(e)}")
        st.info("请确保已安装依赖：pip install -r requirements.txt")

# 开始游戏按钮
if st.button("🎬 开始游戏", type="primary", use_container_width=True):
    run_snake_game()

# 底部提示
st.divider()
st.markdown("""
### ⚠️ 注意事项：
1. 游戏首次加载可能较慢，请耐心等待
2. 请使用**桌面浏览器**（Chrome/Firefox最佳），移动端暂不支持
3. 游戏窗口需要点击激活才能响应键盘操作
4. 若游戏无响应，可刷新页面重新启动
""")