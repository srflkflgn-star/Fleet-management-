import os
import pandas as pd
import streamlit as st

# ገጹ በስልክም ሆነ በኮምፒውተር እንዲመች ማድረግ
st.set_page_config(
    page_title="የስምሪት እና የፍሊት ማኔጅመንት",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# የዳታቤዝ ፋይል ስም (መረጃዎችን በኤክሰል/CSV መልክ ያስቀምጣል)
DATA_FILE = "dispatch_data.csv"

# ፋይሉ ከሌለ አዲስ መፍጠሪያ
if not os.path.exists(DATA_FILE):
    initial_data = pd.DataFrame(
        columns=[
            "የመኪና ሰሌዳ",
            "የአሽከርካሪ ስም",
            "የተነሳበትና መድረሻ",
            "ካርጎ",
            "ነዳጅ (ሊትር)",
            "ሁኔታ",
        ]
    )
    initial_data.to_csv(DATA_FILE, index=False)


def load_data():
    return pd.read_csv(DATA_FILE)


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# ዋና ርዕስ
st.title("🚛 የዕለታዊ የስምሪት መከታተያ ዳሽቦርድ")
st.write("በስልክ እና በኮምፒውተር በቀላሉ የሚሰራ የፍሊት ማኔጅመንት አፕሊኬሽን")

# Sidebar - አዲስ ስምሪት መመዝገቢያ
st.sidebar.header("📝 አዲስ ስምሪት መዝግብ")
with st.sidebar.form("dispatch_form", clear_on_submit=True):
    plate_no = st.text_input("የመኪና ሰሌዳ ቁጥር (e.g. AA 3-12345)")
    driver_name = st.text_input("የአሽከርካሪ ስም")
    route = st.text_input("የተነሳበትና መድረሻ (e.g. አዲስ አበባ ➔ ጂቡቲ)")
    cargo = st.text_input("የካርጎ ዓይነት (e.g. ቡቲ 25 ቶን)")
    fuel = st.number_input("የተሰጠ ነዳጅ (በሊትር)", min_value=0, value=100)
    status = st.selectbox(
        "የስምሪት ሁኔታ",
        [
            "መንገድ ላይ (In Transit)",
            "ዝግጁ (Available)",
            "ጥገና ላይ (Maintenance)",
        ],
    )

    submitted = st.form_submit_button("💾 ስምሪት መዝግብ")

    if submitted and plate_no and driver_name:
        df = load_data()
        new_row = {
            "የመኪና ሰሌዳ": plate_no,
            "የአሽከርካሪ ስም": driver_name,
            "የተነሳበትና መድረሻ": route,
            "ካርጎ": cargo,
            "ነዳጅ (ሊትር)": fuel,
            "ሁኔታ": status,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("መረጃው በስኬት ተመዝግቧል!")

# መረጃዎችን ማሳያ
df_data = load_data()

# የቁጥር ማጠቃለያ (Metrics)
col1, col2, col3, col4 = st.columns(4)
in_transit = len(
    df_data[df_data["ሁኔታ"] == "መንገድ ላይ (In Transit)"]
)
available = len(df_data[df_data["ሁኔታ"] == "ዝግጁ (Available)"])
maintenance = len(df_data[df_data["ሁኔታ"] == "ጥገና ላይ (Maintenance)"])
total_fuel = df_data["ነዳጅ (ሊትር)"].sum() if not df_data.empty else 0

col1.metric("መንገድ ላይ ያሉ", f"{in_transit} መኪኖች")
col2.metric("ዝግጁ የሆኑ", f"{available} መኪኖች")
col3.metric("ጥገና ላይ ያሉ", f"{maintenance} መኪኖች")
col4.metric("ጠቅላላ የተሰጠ ነዳጅ", f"{total_fuel} ሊትር")

st.divider()

# የዳታ ሰንጠረዥ ማሳያ
st.subheader("📋 የተመዘገቡ የስምሪት መረጃዎች")
st.dataframe(df_data, use_container_width=True)

# በኤክሰል ማውረጃ (Export to Excel/CSV)
if not df_data.empty:
    csv = df_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 መረጃዎችን በ Excel (CSV) አውርድ",
        data=csv,
        file_name="dispatch_report.csv",
        mime="text/csv",
    )
