```JSON
{
    "train": {
        "numberOfSample": int,
        "data" : [
            {
                "_id": ,
                "environment": ,
                "activity" : ,
                "sensor_data": [],
                "label":
            },
            ...
        ]
    },
    "validation" : {
        "numberOfSample": int,
        "data" : [
            {
                "_id": ,
                "environment": ,
                "activity" : ,
                "sensor_data": [],
                "label":
            },
            ...
        ]
    },
    "report" : {
        "numberOfSample": int,
        "data" : [
            {
                "_id": ,
                "environment": ,
                "activity" : ,
                "sensor_data": [],
                "label":
            },
            ...
        ]
    }
}
```

OPPURE

```JSON
{
    "trainSample" : ,
    "validationSample" : ,
    "testSample" : ,
    "data" : [
        {
            "_id": ,
            "environment": ,
            "activity" : ,
            "sensor_data": [],
            "label":,
            "type" : "training" | "validation" | "test"
        }
    ]
}
```

Il secondo metodo è più compatto ma molto più caotico a livello di validazione e creazione del dataset