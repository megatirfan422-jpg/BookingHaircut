import streamlit as st
import pandas as pd
import os

# =====================
# SETTINGS
# =====================

BARBER_PASSWORD = "123"
BOOKING_FILE = "bookings.csv"
AVAILABILITY_FILE = "availability.csv"
HISTORY_FILE = "history.csv"

# =====================
# PAGE
# =====================

st.set_page_config(
    page_title="Megat Barber",
    page_icon="💈",
    layout="wide"
)

st.title("💈 MEGAT BARBER")


# =====================
# SOCIAL MEDIA
# =====================

col1, col2, col3 = st.columns(3)

with col1:

    st.link_button(
        "📷 Instagram",
        "https://instagram.com/mgatirfan"
    )

with col2:

    st.link_button(
        "🎵 TikTok",
        "https://tiktok.com/@megatirfan_"
    )

with col3:

    st.link_button(
        "💬 WhatsApp",
        "https://wa.me/60143324491"
    )

st.divider()

# =====================
# PORTFOLIO
# =====================

st.subheader("📸 Portfolio Megat Barber")

portfolio_folder = "portfolio"

if os.path.exists(portfolio_folder):

    images = os.listdir(
        portfolio_folder
    )

    cols = st.columns(3)

    for idx, image in enumerate(images):

        with cols[idx % 3]:

            st.image(
                os.path.join(
                    portfolio_folder,
                    image
                ),
                use_container_width=True
            )

# =====================
# CUSTOMER SECTION
# =====================

 #st.subheader("💈 Selamat Datang ke Megat Barber")


st.header("📅 Customer Booking")

name = st.text_input(
        "Nama"
  )

phone = st.text_input(
        "Telefon"
    )

service = st.selectbox(
        "Servis",
        [
            "Smart Cut",
            "Fade",
            "Haircut + Beard",
            "Beard Trim"
        ]
    )

    


SERVICE_PRICE = {
    "Smart Cut": 15,
    "Fade": 25,
    "Haircut + Beard": 35,
    "Beard Trim": 10
}

if os.path.exists(AVAILABILITY_FILE):

    slot_df = pd.read_csv(
        AVAILABILITY_FILE
    )

    slot_df = slot_df.dropna()

    slot_options = (
    slot_df["date"].astype(str)
    + " | "
    + slot_df["time"].astype(str)
).tolist()

    selected_slot = st.selectbox(
        "Pilih Slot",
        slot_options
    )

else:

    selected_slot = None

    st.warning(
        "Tiada slot tersedia."
    )





if st.button("Book Now"):

    if name == "" or phone == "":
        st.error(
            "Sila isi nama dan telefon."
        )


    else:
        
        from datetime import datetime

        today = datetime.now().strftime("%Y-%m-%d")

        booking_id = "001"

        if os.path.exists(BOOKING_FILE):

            temp_df = pd.read_csv(
                BOOKING_FILE
            )
            
            today_df = temp_df[
               temp_df["date"] == today
            ]
 

            booking_id = f"{len(temp_df)+1:03d}"

        new_booking = pd.DataFrame(
            [[
                booking_id,
                today,
                name,
                phone,
                service,
                selected_slot,
                SERVICE_PRICE[service],
                "Pending"
            ]],
       
    columns=[
               "booking_id",
               "date",
               "name",
               "phone",
               "service",
               "slot",
               "price",
               "status"
]
        )

        if os.path.exists(BOOKING_FILE):

            df = pd.read_csv(
                BOOKING_FILE
            )

            df = pd.concat(
                [df, new_booking],
                ignore_index=True
            )

        else:

            df = new_booking

        df.to_csv(
            BOOKING_FILE,
            index=False
)

# =====================
        # REMOVE BOOKED SLOT
        # =====================

        if os.path.exists(AVAILABILITY_FILE):

            slot_df = pd.read_csv(
                AVAILABILITY_FILE
            )

            selected_parts = str(
                selected_slot
            ).split(" | ")

            if len(selected_parts) == 2:

                selected_date = selected_parts[0]
                selected_time = selected_parts[1]

                slot_df = slot_df[
                    ~(
                        (slot_df["date"].astype(str) == selected_date)
                        &
                        (slot_df["time"].astype(str) == selected_time)
                    )
                ]

                slot_df.to_csv(
                    AVAILABILITY_FILE,
                    index=False
                )

    
        st.success(
            "✅ Booking berjaya dihantar!"
        )
        
        st.info(
            f"📋 Booking ID Anda: {booking_id}"
        )

        st.caption(
            "Simpan Booking ID ini untuk semak status atau cancel booking."
        )

       

# =====================
# CANCEL BOOKING
# =====================

st.divider()

st.subheader("❌ Cancel Booking / Walk-In")

cancel_type = st.radio(
    "Pilih Jenis",
    [
        "Booking",
        "Walk-In"
    ]
)

cancel_booking_id = st.text_input(
    "Masukkan Booking ID / Queue N"
)

if st.button("Cancel Booking / Walk-In"):

    if cancel_type == "Walk-In":

        if os.path.exists("walkin.csv"):

            walkin_df = pd.read_csv(
                "walkin.csv"
            )

            walkin_df = walkin_df[
                walkin_df["queue_id"].astype(str).str.zfill(2)
                != str(cancel_booking_id).zfill(2)
            ]

            walkin_df.to_csv(
                "walkin.csv",
                index=False
            )

            st.success(
                f"✅ Walk-In {cancel_booking_id} berjaya dibatalkan"
            )

        else:

            st.error(
                "❌ Tiada data Walk-In"
            )

    else:

        if os.path.exists(BOOKING_FILE):

            booking_df = pd.read_csv(
                BOOKING_FILE
            )

            match = booking_df[
                booking_df["booking_id"] == cancel_booking_id
            ]

            if not match.empty:

                match.loc[:, "status"] = "Cancelled"

                # RETURN SLOT
                slot_value = str(
                    match.iloc[0]["slot"]
                )

                slot_parts = slot_value.split(" | ")

                if len(slot_parts) == 2:

                    return_slot = pd.DataFrame(
                        [[
                            slot_parts[0],
                            slot_parts[1]
                        ]],
                        columns=[
                            "date",
                            "time"
                        ]
                    )

                    if os.path.exists(
                        AVAILABILITY_FILE
                    ):

                        slot_df = pd.read_csv(
                            AVAILABILITY_FILE
                        )

                        slot_df = pd.concat(
                            [slot_df, return_slot],
                            ignore_index=True
                        )

                    else:

                        slot_df = return_slot

                    slot_df.to_csv(
                        AVAILABILITY_FILE,
                        index=False
                    )

                if os.path.exists(HISTORY_FILE):

                    history_df = pd.read_csv(
                        HISTORY_FILE
                    )

                    history_df = pd.concat(
                        [history_df, match],
                        ignore_index=True
                    )

                else:

                    history_df = match

                history_df.to_csv(
                    HISTORY_FILE,
                    index=False
                )

                booking_df = booking_df[
                    booking_df["booking_id"] != cancel_booking_id
                ]

                booking_df.to_csv(
                    BOOKING_FILE,
                    index=False
                )

                st.success(
                    f"✅ Booking {cancel_booking_id} berjaya dibatalkan"
                )

            else:

                st.error(
                    "❌ Booking ID tidak dijumpai"
                )

        else:

            st.error(
                "❌ Tiada data booking"
            )
# =====================
# CHECK BOOKING STATUS
# =====================

st.divider()

st.subheader("🔍 Check Booking Status")

check_booking_id = st.text_input(
    "Masukkan Booking ID",
    key="check_booking"
)

if st.button("Check Status"):

    found = False

    if os.path.exists(BOOKING_FILE):

        booking_df = pd.read_csv(
            BOOKING_FILE
        )

        match = booking_df[
            booking_df["booking_id"] == check_booking_id
        ]

        if not match.empty:

            st.success(
                f"✅ Status: {match.iloc[0]['status']}"
            )

            found = True

    if (
        not found
        and
        os.path.exists(HISTORY_FILE)
    ):

        history_df = pd.read_csv(
            HISTORY_FILE
        )

        match = history_df[
            history_df["booking_id"] == check_booking_id
        ]

        if not match.empty:

            status = match.iloc[0]["status"]

            if status == "Pending":

                st.warning(
                    f"🟡 Status: {status}"
             )

            elif status == "On Going":

                st.info(
                    f"🔵 Status: {status}"
            )

            elif status == "Completed":

                st.success(
                    f"✅ Status: {status}"
             )

            elif status == "Cancelled":

                st.error(
                    f"❌ Status: {status}"
            )

            else:

                st.write(
                    f"Status: {status}"
            )

            found = True

    if not found:

        st.error(
            "❌ Booking ID tidak dijumpai"
        )
    # =====================
# LIVE QUEUE BOARD
# =====================

st.divider()

st.subheader("🎟️ Queue Board Hari Ini")

if os.path.exists(BOOKING_FILE):

    queue_df = pd.read_csv(
        BOOKING_FILE
    )

    if not queue_df.empty:

        display_df = queue_df[
            [
                "booking_id",
                "name",
                "slot",
                "status"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True
        )

    else:

        st.info(
            "Tiada booking hari ini."
        )

# =====================
# WALK-IN QUEUE
# =====================

    st.divider()


    st.subheader("🚶 Walk-In Queue")

    walkin_name = st.text_input(
        "Nama (Walk-In)",
        key="walkin_name"
    )

    if st.button("🎟️ Ambil Nombor Giliran"):

        queue_id = "01"

        if os.path.exists("walkin.csv"):

            walkin_df = pd.read_csv(
                "walkin.csv"
            )

            queue_id = f"{len(walkin_df)+1:02d}"

        else:

            walkin_df = pd.DataFrame(
                columns=[
                    "queue_id",
                    "name",
                    "status"
                ]
            )

        new_walkin = pd.DataFrame(
            [[
                queue_id,
                walkin_name,
                "Waiting"
            ]],
            columns=[
                "queue_id",
                "name",
                "status"
            ]
        )

        walkin_df = pd.concat(
            [walkin_df, new_walkin],
            ignore_index=True
        )

        walkin_df.to_csv(
            "walkin.csv",
            index=False
        )

        st.success(
               f"🎟️ Nombor Giliran Anda: {queue_id}"
    )

st.subheader("📺 Walk-In Queue Live")

if os.path.exists("walkin.csv"):

    walkin_df = pd.read_csv(
        "walkin.csv"
    )

    st.dataframe(
        walkin_df,
        use_container_width=True
    )
# =====================
# BARBER LOGIN
# =====================

st.divider()

st.header("✂️ Barber Login")

password = st.text_input(
    "Password",
    type="password"
)

if password == BARBER_PASSWORD:

    st.success("Login berjaya ✅")
    

    # =====================
    # DASHBOARD SUMMARY
    # =====================
    
# =====================
    # WALK-IN MANAGEMENT
    # =====================

    st.subheader("🚶 Walk-In Queue")
    
    # =====================
    # CANCEL WALK-IN
    # =====================

    st.subheader("❌ Cancel Walk-In")

    cancel_walkin_id = st.text_input(
        "Masukkan Nombor Walk-In",
        key="cancel_walkin"
    )

    if st.button("Cancel Walk-In"):

        if os.path.exists("walkin.csv"):

            walkin_df = pd.read_csv(
                "walkin.csv"
            )

            if cancel_walkin_id in walkin_df["queue_id"].astype(str).values:

                walkin_df = walkin_df[
                    walkin_df["queue_id"] != cancel_walkin_id
                ]

                walkin_df.to_csv(
                    "walkin.csv",
                    index=False
                )

                st.success(
                    f"✅ Walk-In {cancel_walkin_id} berjaya dibatalkan"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Nombor Walk-In tidak dijumpai"
                )

        else:

            st.error(
                "❌ Tiada data Walk-In"
            )

    if os.path.exists("walkin.csv"):

        walkin_df = pd.read_csv(
            "walkin.csv"
        )

        st.dataframe(
            walkin_df,
            use_container_width=True
        )

        if not walkin_df.empty:

            selected_walkin = st.selectbox(
                "Pilih Walk-In",
                walkin_df.index,
                key="walkin_status"
            )

            walkin_status = st.selectbox(
                "Status Walk-In",
                [
                    "Waiting",
                    "On Going",
                    "Completed"
                ]
            )

            if st.button("✅ Update Walk-In"):

                walkin_df.loc[
                    selected_walkin,
                    "status"
                ] = walkin_status

                if walkin_status == "Completed":

                    walkin_df = walkin_df.drop(
                        selected_walkin
                    )

                    walkin_df = walkin_df.reset_index(
                        drop=True
                    )

                walkin_df.to_csv(
                    "walkin.csv",
                    index=False
                )

                st.success(
                    "✅ Walk-In berjaya dikemaskini"
                )

                st.rerun()    
    active_count = 0
    history_count = 0
    total_income = 0

    if os.path.exists(BOOKING_FILE):

        booking_df = pd.read_csv(
            BOOKING_FILE
        )

        active_count = len(
            booking_df
        )

    if os.path.exists(HISTORY_FILE):

        history_df = pd.read_csv(
            HISTORY_FILE
        )

        history_count = len(
            history_df
        )

        if (
            "status" in history_df.columns
            and
            "price" in history_df.columns
        ):

            completed_df = history_df[
                history_df["status"] == "Completed"
            ]

            total_income = completed_df[
                "price"
            ].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📋 Active Booking",
            active_count
        )

    with col2:
        st.metric(
            "📜 History",
            history_count
        )

    with col3:
        st.metric(
            "💰 Income",
            f"RM {total_income}"
        )

    # =====================
    # ADD SLOT
    # =====================

    st.subheader("➕ Add Availability Slot")

    slot_date = st.text_input(
        "Tarikh Slot",
        key="slot_date"
    )

    slot_time = st.text_input(
        "Masa Slot",
        key="slot_time"
    )

    if st.button("Add Slot"):

        new_slot = pd.DataFrame(
            [[slot_date, slot_time]],
            columns=["date", "time"]
        )

        if os.path.exists(AVAILABILITY_FILE):

            df_slot = pd.read_csv(
                AVAILABILITY_FILE
            )

            df_slot = pd.concat(
                [df_slot, new_slot],
                ignore_index=True
            )

        else:

            df_slot = new_slot

        df_slot.to_csv(
            AVAILABILITY_FILE,
            index=False
        )

        st.success("✅ Slot berjaya ditambah")
        st.rerun()
    # =====================
    # AVAILABLE SLOT
    # =====================

    st.subheader("📅 Available Slots")

    if os.path.exists(AVAILABILITY_FILE):

        slot_df = pd.read_csv(
            AVAILABILITY_FILE
        )

        st.dataframe(
            slot_df,
            use_container_width=True
        )
        # =====================
        # DELETE SLOT
        # =====================

        if not slot_df.empty:

            delete_slot = st.selectbox(
                "Pilih Slot Untuk Dipadam",
                (
                    slot_df["date"].astype(str)
                    + " | "
                    + slot_df["time"].astype(str)
                ).tolist(),
                key="delete_slot"
            )

            if st.button("🗑️ Delete Slot"):

                selected_parts = delete_slot.split(" | ")

                selected_date = selected_parts[0]
                selected_time = selected_parts[1]

                slot_df = slot_df[
                    ~(
                        (slot_df["date"].astype(str) == selected_date)
                        &
                        (slot_df["time"].astype(str) == selected_time)
                    )
                ]

                slot_df.to_csv(
                    AVAILABILITY_FILE,
                    index=False
                )

                st.success(
                    "✅ Slot berjaya dipadam"
                )

                st.rerun()
# =====================
    # BOOKING TABLE
    # =====================

    st.subheader("📋 Semua Booking")

    if os.path.exists(BOOKING_FILE):

        df = pd.read_csv(
            BOOKING_FILE
        )

        # =====================
        # QUEUE HARI INI
        # =====================

        if not df.empty:

            st.subheader("🎟️ Queue Hari Ini")

            queue_df = df[
                [
                    "booking_id",
                    "name",
                    "status"
                ]
            ]

            st.dataframe(
                queue_df,
                use_container_width=True
            )

        st.dataframe(
            df,
            use_container_width=True
        )

        if not df.empty:

            selected_customer = st.selectbox(
                "Pilih Customer",
                df.index
            )

            new_status = st.selectbox(
                "Update Status",
                [
                    "Pending",
                    "Confirmed",
                    "On Going",
                    "Completed",
                    "Cancelled"
                ]
            )

            if st.button("Update Status"):

                df.loc[
                    selected_customer,
                    "status"
                ] = new_status

                if new_status in [
                    "Completed",
                    "Cancelled"
                ]:

                    selected_row = df.loc[
                        [selected_customer]
                    ].copy()

                    selected_row.loc[
                        :,
                        "status"
                    ] = new_status

                    if os.path.exists(HISTORY_FILE):

                        history_df = pd.read_csv(
                            HISTORY_FILE
                        )

                        history_df = pd.concat(
                            [history_df, selected_row],
                            ignore_index=True
                        )

                    else:

                        history_df = selected_row

                    history_df.to_csv(
                        HISTORY_FILE,
                        index=False
                    )

                    df = df.drop(
                        index=selected_customer
                    )

                    df = df.reset_index(
                        drop=True
                    )

                df.to_csv(
                    BOOKING_FILE,
                    index=False
                )

                st.success(
                    "✅ Status berjaya dikemaskini"
                )

                st.rerun()

    else:

        st.info(
            "Tiada booking lagi."
        )
    # =====================
    # HISTORY
    # =====================

    st.subheader("📜 History")

    if os.path.exists(HISTORY_FILE):

        history_df = pd.read_csv(
            HISTORY_FILE
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

        if not history_df.empty:

            selected_history = st.selectbox(
                "Pilih History Untuk Padam",
                history_df.index,
                key="history_delete"
            )

            if st.button("🗑️ Delete History"):

                history_df = history_df.drop(
                    selected_history
                )

                history_df.to_csv(
                    HISTORY_FILE,
                    index=False
                )

                st.success(
                    "✅ History berjaya dipadam"
                )

                st.rerun()

        # =====================
        # INCOME
        # =====================

        st.subheader("💰 Income Summary")

        if (
            "status" in history_df.columns
            and
            "price" in history_df.columns
        ):

            completed_df = history_df[
                history_df["status"] == "Completed"
            ]

            cancelled_df = history_df[
                history_df["status"] == "Cancelled"
            ]

            total_income = completed_df[
                "price"
            ].sum()

            completed_count = len(
                completed_df
            )

            cancelled_count = len(
                cancelled_df
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "💰 Total Income",
                    f"RM {total_income}"
                )

            with col2:
                st.metric(
                    "✅ Completed",
                    completed_count
                )

            with col3:
                st.metric(
                    "❌ Cancelled",
                    cancelled_count
                )

    else:

        st.info(
            "Tiada history lagi."
        )