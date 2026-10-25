import json
          import os
          import uuid
          import base64
          import boto3
          from datetime import datetime, timezone

          s3 = boto3.client("s3")
          table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

          def response(status, body):
              return {
                  "statusCode": status,
                  "headers": {"Content-Type": "application/json"},
                  "body": json.dumps(body)
              }

          def handler(event, context):
              method = event.get("httpMethod", "")
              path = event.get("resource", "")

              if method == "POST" and path == "/files":
                  try:
                      data = json.loads(event.get("body") or "{}")
                      filename = os.path.basename(data["filename"])
                      content = data["content"]
                      if not filename or not isinstance(content, str):
                          return response(400, {"error": "filename and string content are required"})
                      file_id = str(uuid.uuid4())
                      key = file_id + "/" + filename
                      s3.put_object(
                          Bucket=os.environ["BUCKET_NAME"],
                          Key=key,
                          Body=content.encode("utf-8"),
                          ContentType="text/plain"
                      )
                      item = {
                          "fileId": file_id,
                          "filename": filename,
                          "s3Key": key,
                          "status": "PROCESSED",
                          "createdAt": datetime.now(timezone.utc).isoformat()
                      }
                      table.put_item(Item=item)
                      return response(201, item)
                  except (KeyError, TypeError, ValueError) as exc:
                      return response(400, {"error": str(exc)})

              if method == "GET" and path == "/status/{fileId}":
                  file_id = (event.get("pathParameters") or {}).get("fileId")
                  if not file_id:
                      return response(400, {"error": "fileId is required"})
                  result = table.get_item(Key={"fileId": file_id})
                  item = result.get("Item")
                  if not item:
                      return response(404, {"error": "file not found"})
                  return response(200, item)

              return response(404, {"error": "route not found"})

