def chunk_document(
    documents:list[dict], chunk_size: int = 500, chunking_overlap: int = 50
) -> list[dict]:


    chunks =[]

    for document in documents:
        content = document["content"]
        source = document["source"]

        start = 0

        while start < len(content):
            end = start+chunk_size
            chunk = content[start:end]

            chunks.append(
                {
                    'content': chunk,
                    'source':source
                }
            )
            start =end -chunking_overlap


    return chunks



