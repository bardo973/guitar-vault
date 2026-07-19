# --- VISUALIZZAZIONE ---
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Il vault è vuoto.")
else:
    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    st.image(row['foto_path'], width=150)
                st.subheader(f"{row['marca']} {row['modello']}")
                st.caption(f"S/N: {row['serie']}")
            
            with col2:
                st.write(f"**Corde:** {row['corde']}")
                data_scadenza = datetime.strptime(row['prossimo_cambio'], "%Y-%m-%d").date()
                if data_scadenza <= datetime.now().date():
                    st.error(f"⚠️ Cambio necessario dal {row['prossimo_cambio']}")
                else:
                    st.info(f"📅 Prossimo cambio: {row['prossimo_cambio']}")
            
            with col3:
                # Bottone Modifica
                with st.popover("Modifica"):
                    with st.form(f"form_edit_{row['id']}"):
                        new_marca = st.text_input("Marca", value=row['marca'])
                        new_modello = st.text_input("Modello", value=row['modello'])
                        new_serie = st.text_input("S/N", value=row['serie'])
                        new_corde = st.text_input("Corde", value=row['corde'])
                        if st.form_submit_button("Salva modifiche"):
                            conn = sqlite3.connect(DB_NAME)
                            conn.execute("UPDATE chitarre SET marca=?, modello=?, serie=?, corde=? WHERE id=?",
                                         (new_marca, new_modello, new_serie, new_corde, row['id']))
                            conn.commit()
                            conn.close()
                            st.rerun()

                if st.button("Fatto! Cambio corde", key=f"btn_{row['id']}"):
                    nuovo_cambio = datetime.now().date()
                    nuova_scadenza = nuovo_cambio + timedelta(days=90)
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("UPDATE chitarre SET data_cambio = ?, prossimo_cambio = ? WHERE id = ?", 
                                 (str(nuovo_cambio), str(nuova_scadenza), row['id']))
                    conn.commit()
                    conn.close()
                    st.rerun()
                
                if st.button("Elimina", key=f"del_{row['id']}"):
                    delete_guitar(row['id'])
                    st.rerun()