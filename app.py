st.markdown("#### Specifiche Tecniche")
    s1, s2 = st.columns(2)
    body = s1.text_input("Body", value=selected_guitar.get("body", "") if selected_guitar else "")
    neck = s2.text_input("Manico / Profilo", value=selected_guitar.get("neckWood", "") if selected_guitar else "")
    
    # 3 colonne corrette: s3, s4, s5
    s3, s4, s5 = st.columns(3)
    fretboard = s3.text_input("Tastiera", value=selected_guitar.get("fretboard", "") if selected_guitar else "")
    pickups = s4.text_input("Pickups", value=selected_guitar.get("pickups", "") if selected_guitar else "")
    hardware = s5.text_input("Hardware / Ponte", value=selected_guitar.get("hardware", "") if selected_guitar else "")