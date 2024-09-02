def writeClusters(name: str, comments: list[str], labels: list[int]):
    # Открываем файл для записи
    with open(f"{name}.txt", 'w', encoding='utf-8') as file:
        # Находим уникальные метки
        unique_labels = set(labels)
        
        # Проходим по каждой уникальной метке
        for label in unique_labels:
            # Отбираем комментарии, соответствующие текущей метке
            label_comments = [comments[i] for i in range(len(comments)) if labels[i] == label]
            
            # Записываем метку
            file.write(f"=Номер Label {label}==========\n")
            
            # Записываем комментарии
            for comment in label_comments:
                file.write(f"{comment}\n")
                
            # Записываем количество комментариев в данной метке
            file.write(f"\n=Количество комментариев в label {label}==== {len(label_comments)}=\n\n")