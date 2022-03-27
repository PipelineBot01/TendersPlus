##### Model
```bash
├── conf
│   ├── division.py # division-id mapping file
│   ├── features.py # tenders' feature configuration file
│   └── file_path.py # all dataset files' path
├── relation_interface
│   └── Relation.py # matching class interface
├── researcher
│   ├── assets 
│   │   ├── researcher_division.csv # researcher-div mapping df
│   │   ├── researcher_info.csv # researcher info df
│   │   ├── researcher_tag.csv # researcher-tag mapping df
│   │   └── tag_category_map.csv # tag-div mapping df
│   └── matching
│   │   └── researcher_relation.py # researcher matching class 
│   └── output # test output
│   │   └──assessment # model result assessment
├── tenders
│   ├── assets 
│   │   ├── matching_result_by_lda.csv # tenders-topic info df
│   │   ├── matching_topics_by_lda.csv # topic-word mapping df
│   │   ├── tenders_info.csv # tenders info df
│   │   ├── tenders_keyword.csv # tenders-keyword info df
│   │   ├── tenders_tag.csv # tenders-keyword mapping df
│   │   └── tenders_topic.csv # tenders-topic info mapping df 
│   ├── features
│   │   ├── lda_model.py # tenders' topic extractor class
│   │   ├── tenders_feat_creator.py # tenders' mapping df generating class
│   │   └── tenders_key_extractor.py # tenders' keywords extractor class
│   └── matching
│   │   └── tenders_relation.py # tenders matching class 
│   └── output # test matching output
│   │   └──assessment # model result assessment
└─ utils
   ├── feature_utils.py # feature related util functions set
   ├── match_utils.py # matching related util functions set
   └── tool_utils.py # tool functions set
