openapi: 3.0.0
info:
  title: Offers API
  version: v1

servers:
  - url: /cxm/prospect

paths:
  /offers:
    post:
      summary: Get offers based on visitor information
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OfferRequest'
      responses:
        '200':
          description: Successful response (details of the response will depend on your actual API)
          content:
            application/json:
              # Define your success response schema here if you have one
              example:
                offers: []
        '400':
          description: Bad Request
          content:
            application/json:
              example:
                error: "Invalid input"
        '500':
          description: Internal Server Error
          content:
            application/json:
              example:
                error: "Internal server error"

components:
  schemas:
    GlobalRequest:
      type: object
      properties:
        client_identifier:
          type: string
          description: Identifier of the client
          example: ASPEN
        request_identifier:
          type: string
          description: Identifier of the request
          example: CS-ASPEN-OMI
        locale:
          type: string
          description: Locale of the request
          example: en-US
        request_ts:
          type: string
          format: date-time
          description: Timestamp of the request
          example: 2023-03-22T17:19:54.014-0700
        request_type:
          type: string
          description: Type of the request
          example: offers/traits

    VisitorInfo:
      type: object
      properties:
        pznid:
          type: string
          description: Visitor identifier
          example: 27732220528357082048435368852113564596|9
        hmid:
          type: string
          description: Hashed visitor identifier
          example: 6cc9f96ab2391460eae12e53704a6f7f400899a76aea85d9185bdd613647678d
        encrypted:
          type: string
          description: Indicates if visitor info is encrypted
          enum:
            - Yes
            - No
          example: Yes

    OfferRequest:
      type: object
      properties:
        global_request:
          $ref: '#/components/schemas/GlobalRequest'
        visitor_info:
          $ref: '#/components/schemas/VisitorInfo'
      required:
        - global_request
        - visitor_info
