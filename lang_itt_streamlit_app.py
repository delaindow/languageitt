import streamlit as st
import re
import tempfile
import zipfile
import os

def process_itt(file_content, lang_code):
    """Modify the .itt file by updating the language code and replacing text with 'TRANSLATED TEXT HERE'."""
    # Update xml:lang attribute
    updated_content = re.sub(r'xml:lang="[a-zA-Z-]+"', f'xml:lang="{lang_code}"', file_content)
    
    # Replace text inside <p> tags with 'TRANSLATED TEXT HERE'
    updated_content = re.sub(r'(<p[^>]*>)(.*?)(</p>)', r'\1TRANSLATED TEXT HERE\3', updated_content, flags=re.DOTALL)
    
    return updated_content

def main():
    st.title(".ITT File Translator")
    
    # Upload file
    uploaded_file = st.file_uploader("Upload an English .itt file", type=["itt"])
    
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        
        # Language selection
        languages = {
            "Italian": "it",
            "Spanish": "es-ES",
            "French": "fr",
            "Korean": "ko",
            "Indonesian": "id"
        }
        
        selected_langs = st.multiselect("Select languages to download:", list(languages.keys()))
        if st.button("Generate ZIP Download"):
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "translated_files.zip")
                
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for selected_lang in selected_langs:
                        lang_code = languages[selected_lang]
                        modified_content = process_itt(file_content, lang_code)
                        
                        # Save to a temporary file
                        itt_filename = f"translated_{lang_code}.itt"
                        itt_path = os.path.join(temp_dir, itt_filename)
                        with open(itt_path, "w", encoding="utf-8") as f:
                            f.write(modified_content)
                        
                        # Add to ZIP
                        zipf.write(itt_path, itt_filename)
                
                # Provide download link for ZIP
                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="Download All Translated Files (ZIP)",
                        data=f,
                        file_name="translated_files.zip",
                        mime="application/zip"
                    )

if __name__ == "__main__":
    main()
