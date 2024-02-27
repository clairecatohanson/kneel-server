import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from managers import get_all_orders, get_single_order, create_order, delete_order
from managers import update_metal


class JSONServer(HandleRequests):
    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "orders":
            if url["pk"] != 0:
                response_body = get_single_order(url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                response_body = get_all_orders(url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "orders":
            if url["pk"] != 0:
                return self.response(
                    "Incorrect request format. Posted data will autoincrement. Do not provide a primary key.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            else:
                successfully_created = create_order(request_body)
                if successfully_created:
                    return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
                else:
                    return self.response(
                        "Error. Data was not successfully posted.",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
        else:
            return self.response(
                "",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_PUT(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        response_body = self.rfile.read(content_len)
        response_body = json.loads(response_body)

        if url["requested_resource"] == "metals":
            if url["pk"] == 0:
                return self.response(
                    "Incorrect request format. Please provide a primary key.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            else:
                successfully_updated = update_metal(url, response_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                else:
                    return self.response(
                        "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )

    def do_DELETE(self):
        url = self.parse_url(self.path)

        if url["requested_resource"] == "orders":
            if url["pk"] == 0:
                return self.response(
                    "Incorrect request format. Please provide a primary key.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
            else:
                successfully_deleted = delete_order(url)
                if successfully_deleted:
                    return self.response(
                        "",
                        status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value,
                    )
                else:
                    return self.response(
                        "Deletion not successful",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
