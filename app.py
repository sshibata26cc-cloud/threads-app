import streamlit as st
import time

# --- ページ基本設定 ---
st.set_page_config(
    page_title="画像生成 & 自動投稿ダッシュボード",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- タイトル & ヘッダー ---
st.title("🎨 AI画像生成 & 投稿ダッシュボード")
st.caption("AIで画像を生成し、そのままGoogleビジネスプロフィールやSNSへ投稿・管理できます。")

# --- セッション状態（生成画像や投稿履歴の保持）の初期化 ---
if "generated_image_url" not in st.session_state:
    st.session_state.generated_image_url = None
if "post_history" not in st.session_state:
    st.session_state.post_history = []

# --- サイドバー：設定エリア ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("API Key", type="password", help="画像生成モデルのAPIキーを入力してください")
    
    st.divider()
    
    st.subheader("📌 投稿先アカウント")
    target_platform = st.selectbox(
        "プラットフォーム選択",
        ["Google Business Profile (GBP)", "Instagram", "X (旧Twitter)", "Facebook"]
    )
    
    selected_location = st.selectbox(
        "対象店舗 / ページ",
        ["店舗A（福岡天神店）", "店舗B（博多駅前店）", "テストアカウント"]
    )

# --- メインコンテンツ領域（2カラム構成） ---
col_left, col_right = st.columns([1, 1], gap="large")

# ----------------------------------------------------
# 左カラム：画像生成 & 投稿作成エリア
# ----------------------------------------------------
with col_left:
    st.subheader("1. 🎨 AI画像生成プロンプト")
    
    # 画像生成入力
    prompt = st.text_area(
        "プロンプト（画像のイメージを入力）",
        placeholder="例: 美味しそうなガーリックラーメン、湯気が立っている、高画質、フード写真風",
        height=100
    )
    
    col_aspect, col_style = st.columns(2)
    with col_aspect:
        aspect_ratio = st.selectbox("アスペクト比", ["1:1 (正方形)", "16:9 (横長)", "9:16 (縦長)"])
    with col_style:
        style = st.selectbox("スタイル", ["リアル写真風", "イラスト", "水彩画風", "3Dレンダリング"])

    # 画像生成ボタン
    if st.button("✨ 画像を生成する", use_container_width=True, type="primary"):
        if not prompt:
            st.warning("プロンプトを入力してください。")
        else:
            with st.spinner("AIが画像を生成中..."):
                # --------------------------------------------------------
                # ※ここに実際の画像生成API（DALL-E 3 / Flux / Midjourney等）の処理が入ります。
                # 今回はデモ用のダミー画像を表示します。
                time.sleep(2)
                # --------------------------------------------------------
                st.session_state.generated_image_url = "https://picsum.photos/600/600" # デモ用プレースホルダー
                st.success("画像の生成が完了しました！")

    st.divider()

    st.subheader("2. 📝 投稿文作成 & 設定")
    post_text = st.text_area(
        "投稿キャプション・説明文",
        placeholder="例: 今週のオススメメニュー！新鮮なニンニクをたっぷり使った自慢の一品です。ご来店お待ちしております！",
        height=120
    )

    col_topic, col_cta = st.columns(2)
    with col_topic:
        topic_type = st.selectbox("投稿タイプ (GBP)", ["標準投稿 (最新情報)", "イベント", "特典・オファー"])
    with col_cta:
        cta_type = st.selectbox("コール トゥ アクション (CTA)", ["なし", "詳細", "予約", "オンライン注文", "電話"])

# ----------------------------------------------------
# 右カラム：プレビュー & 投稿実行エリア
# ----------------------------------------------------
with col_right:
    st.subheader("3. 👁️ 投稿プレビュー")
    
    # 画像プレビュー表示
    if st.session_state.generated_image_url:
        st.image(st.session_state.generated_image_url, caption="生成された画像", use_container_width=True)
    else:
        st.info("左側のフォームから画像を生成すると、ここにプレビューが表示されます。")

    # 投稿本文プレビュー
    if post_text:
        st.markdown("**【本文プレビュー】**")
        st.info(post_text)

    st.divider()

    st.subheader("4. 🚀 投稿アクション")
    
    col_submit_now, col_schedule = st.columns(2)
    
    with col_submit_now:
        # 即時投稿ボタン
        if st.button("📤 今すぐ投稿する", use_container_width=True):
            if not st.session_state.generated_image_url:
                st.error("投稿する画像がありません。画像を生成してください。")
            elif not post_text:
                st.error("投稿本文を入力してください。")
            else:
                with st.spinner("投稿を送信中..."):
                    # --------------------------------------------------------
                    # ※ここに実際のGBP/SNS投稿処理API（`create_post`等）が入ります。
                    time.sleep(1.5)
                    # --------------------------------------------------------
                    st.session_state.post_history.append({
                        "time": time.strftime("%Y-%m-%d %H:%M"),
                        "platform": target_platform,
                        "location": selected_location,
                        "text": post_text[:30] + "..."
                    })
                    st.balloons()
                    st.success(f"{target_platform}（{selected_location}）へ正常に投稿されました！")

    with col_schedule:
        # 予約投稿ボタン（ダイアログ風簡易実装）
        if st.button("📅 予約投稿", use_container_width=True):
            st.info("予約投稿機能は準備中です。")

# --- 下部：投稿履歴エリア ---
st.divider()
st.subheader("📜 投稿実行履歴")
if st.session_state.post_history:
    st.table(st.session_state.post_history)
else:
    st.caption("まだ実行された投稿はありません。")
