from main import extract_logs

def test_extract_logs_not_json():

    event = {
        "attributes": {
            "bucketId": "bucket",
            "objectId": "not-json.txt"
        }
    }
    context = None

    result = extract_logs(event, context)

    assert result is None
