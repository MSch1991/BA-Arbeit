# Korpuserstellung und Algorithmen für Eigennamenerkennung auf deutschen Stellenanzeigen #

## Preprocessing ##
7. split_conll.py  
   Teilt eine "<file_name>\_<data_set>.conll" Datei in "<file_name>\_<data_set>\_PER.conll",
   "<file_name>\_<data_set>\_ORG.conll" und "<file_name>\_<data_set>\_LOC.conll" auf. Z.B. enthält
   die PER.conll alle Worte aus der Eingabedatei, aber jede Annotation die nicht PER ist wurde durch
   O ersetzt.
   <br><br>
   **Nutzung:**   
   <code>python split_conll.py <corpora_path> <file_name></code>

### Benikova ###
6. germaner_preprocessor.py
   Entfernt die Kategorie "OTH" aus dem Datensatz und wandelt die Unterkategorien -part und -deriv in normale Kategorien um. 
   Nutzung:  
   <code>python germaner_preprocesor.py <conll_directory> <prefix></code>

### My Data ###

1. empty_lines.py  
   Trennt die Sätze des Datensatzes und fügt dazwischen leere Zeilen ein.
   **Nutzung**:  
   <code>python empty_lines.py <all_corpus> <new_corpus></code>

#### Dev ####
2. tagtog_format_anno.py  
   Wandelt die annotierte Datei in eine Datei vom CSV-Format um. 
   **Nutzung**:  
   <code>python tagtog_format_anno.py <source_dir> <target_dir></code>
   
   tagtog_format_unanno.py  
   Wandelt die unannotierte Datei in eine Datei vom CSV-Format um. 
   **Nutzung**:  
   <code>python tagtog_format_unanno.py <source_dir> <target_dir></code>
   
3. merge_token_files.py  
   Mappt die leeren Zeilen in der unannotierten Datei auf die annotierte Datei.
   **Nutzung**:  
   <code>python merge_token_files.py <source_dir_1> <source_dir_2> <target_dir></code>
   
4. concat_entities.py  
   Konkateniert alle 3 Enitity-Kategorien, damit der Datensatz nicht nur mit einer Kategorie annotiert ist, sondern mit allen.
   **Nutzung**:  
   <code>python concat_entities.py <source_dir> <target_dir></code>
   

Train
5. GermaNER-nofb-09-09-2015.jar (see https://github.com/AIPHES/GermaPOS)  
   Anwendung des GermaNER Recognition Tool auf das Trainingsdaten Set  um eine automatische Annotation durchzuführen.  
   **Nutzung**:  
   <code>java -Xmn4g -Xmx4g -jar GermaNER-nofb-09-09-2015.jar -t <input_file> -o <output_file> </code>

#### Test ####
2. tagtog_format_anno.py  
   Wandelt die annotierte Datei in eine Datei vom CSV-Format um. 
   **Nutzung**:  
   <code>python tagtog_format_anno.py <source_dir> <target_dir></code>
   
   tagtog_format_unanno.py  
   Wandelt die unannotierte Datei in eine Datei vom CSV-Format um.
   **Nutzung**:  
   <code>python tagtog_format_unanno.py <source_dir> <target_dir></code>
   
3. merge_token_files.py  
   Mappt die leeren Zeilen in der unannotierten Datei auf die annotierte Datei.
   **Nutzung**:  
   <code>python merge_token_files.py <source_dir_1> <source_dir_2> <target_dir></code>
   
4. concat_entities.py  
   Konkateniert alle 3 Enitity-Kategorien, damit der Datensatz nicht nur mit einer Kategorie annotiert ist, sondern mit allen.
   **Nutzung**:  
   <code>python concat_entities.py <source_dir> <target_dir></code>
   


## Sequence Tagging Transfer ##

Geklont von https://github.com/riedlma/sequence_tagging#download-models-and-embeddings.
Leichte Anpassungen bezüglich der Abhängigkeiten und des Codes wurden durchgeführt. Anleitung für Benutzung
kann im orginalen Repository gefunden werden. Ein kleines Beispiel für das Transfer Learning
befindet sich weiter unten.

### corpora ###
Hier befinden sich die Korpora. z.B.
* benikova_dev.conll
* benikova_dev_LOC.conll
* ...
* benikova_train_PER.conll

### embeddings ###
wiki.de.bin (see https://fasttext.cc/docs/en/pretrained-vectors.html German)

### model_benikova ###
Ordner enthalt die Konfigration für das Modell für die Daten von Benikova. Nach ausführen von build_data und train
befinden sich hier auch die notwenidgen Vokabularsdaten und die trainierten Gewichte des neuronales Netzwerkes.

### model_my_data ###
Ordner enthalt die Konfigration für das Modell für die Daten von mir. Nach ausführen von build_data und train
befinden sich hier auch die notwenidgen Vokabularsdaten und die trainierten Gewichte des neuronales Netzwerkes.

## Transfer Learning ##

Für transfer learning von benikova auf my_data wurde Grundstruktur verwendet. Über die Konfigurationsdatei
und Anpassung der Befehle können verschiedene Szenarien ausgewertet werden.  

<code>
python build_data.py model_benikova/config corpora/my_data/my_data_train.conll corpora/my_data/my_data_dev.conll corpora/my_data/my_data_test.conll<br>
python train.py model_benikova/config<br>
python transfer_learning.py model_benikova/config corpora/my_data/my_data_train.conll corpora/my_data/my_data_dev.conll<br>
python evaluate.py model_benikova/config
</code>
