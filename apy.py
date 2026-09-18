import streamlit as st 
import pandas as pd 
from supabase import create_client

a,b,c=st.columns([2,2,1.5])
with b :

    st.header("Dashboard")

st.set_page_config(

    page_title="dashboard" ,
    page_icon="📊",
    layout="wide"

)

SUPABASE_URL="https://elxxxjktovtgoavpvovx.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVseHh4amt0b3Z0Z29hdnB2b3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkxNDY2NzcsImV4cCI6MjEwNDcyMjY3N30.PlMTKPKzOf-yvh1MtUEsZdxdqDeiChhaSSKxBAXam4I"

@st.cache_resource

def init_supabase () :

    return create_client(supabase_url=SUPABASE_URL,supabase_key=SUPABASE_KEY)

supabase=init_supabase()

try : 

    response=supabase.table("registrations").select("*").execute()
    raw_data=response.data

    if raw_data :

        # home fille now

        df=pd.DataFrame(raw_data)
        st.success("تم جلب البيانات بنجاح !")

        total_all=len(df)
        total_3=len(df[df['age']==3])
        total_4=len(df[df['age']==4])
        total_5=len(df[df['age']==5])
        total_other=total_all-(total_3+total_4+total_5)

        col1,col2,col3,col4,col5=st.columns(5)



        with col1 :

            st.metric(label="إجمالي التلاميذ",value=total_all)

        with col2 :

            st.metric(label="عدد التلاميذ 3 سنوات",value=total_3)

        with col3 :

            st.metric(label="عدد التلاميذ 4 سنوات ",value=total_4)

        with col4 : 

            st.metric(label="عدد التلاميذ 5 سنوات",value=total_5)

        with col5 :

            st.metric(label="عدد التلاميذ من الأعمار أقل من أو أكثر مماهو مذكور",value=total_other)

        st.markdown("---")

        select_age=st.selectbox(
            "التصفية حسب الفئة العمرية",
            ["all",5,4,3,2,1]
        )

        l1,l2,l3=st.columns([1,2,1])

        with l2 :

            search_query=st.text_input("البحث عن التلميذ بالإسم أواللقب أو رقم التلميذ (id):")

        filtered_df = df.copy()

        if select_age != "all" :

            search_str=str(search_query).strip()

            filtered_df = filtered_df[filtered_df["age"]==select_age]

        if search_query :

            comd_id=filtered_df["id"].astype(str).str.contains(search_query,case=False,na=False)
            comd_name=filtered_df["name"].astype(str).str.contains(search_query,case=False,na=False)
            comd_sd_name=filtered_df["second_name"].astype(str).str.contains(search_query,case=False,na=False)
            filtered_df=filtered_df[comd_id|comd_name|comd_sd_name]

        st.write(f"إجمالي التلاميذ بعد البحث:**{len(filtered_df)}**")

        df_to_show = filtered_df.drop(columns=["created_at"])

        edited_df=st.dataframe(df_to_show,
                                 use_container_width=True,
                                  hide_index=True )

    else :

        st.info("الإتصال ناجح لكن لا توجد بيانات حاليا")

except Exception as e :

    st.error(f"حدث خطأ أثناء جلب البيانات :{e}")





