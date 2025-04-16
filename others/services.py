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
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OfferResponse'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

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

    GlobalResponse:
      type: object
      properties:
        request_identifier:
          type: string
          description: Identifier of the request
          example: CS-ASPEN-OM
        explanation_code:
          type: string
          description: Explanation code for the response
          example: OMI0000
        explanation_message:
          type: string
          description: Explanation message for the response
          example: Success/Failure
        response_ts:
          type: string
          format: date-time
          description: Timestamp of the response
          example: 2025-04-10T17:19:54.076-0700

    VisitorIdentity:
      type: object
      properties:
        hmid:
          type: string
          description: Hashed visitor identifier
          example: 6cc9f96ab2391460eae12e53704a6f7f400899a76aea85d9185bdd613647678d
        pznId:
          type: string
          description: Visitor identifier
          example: 27732220528357082048435368852113564596|9
        cmInd:
          type: string
          description: Customer match indicator (Y/N)
          example: "(Y/N)"
        pin:
          type: string
          description: PIN
          example: "999185bdd613647643"
        custXrefId:
          type: string
          description: Customer cross-reference ID
          example: J56255GFREE484353688521135
        gctId:
          type: string
          description: Global customer tracking ID
          example: J56255GFREddsdkskdjsE484353688521135d7787
        last_updated_ts:
          type: string
          format: date-time
          description: Timestamp of the last update
          example: 2025-05-10T17:19:54.076-0700

    Offer:
      type: object
      properties:
        iaCode:
          type: string
          description: IA Code
          example: ""
        sourceCode:
          type: string
          description: Source Code
          example: "#Aspen will populate outgoing EEP here"
        startDt:
          type: string
          description: Start Date
          example: ""
        endDt:
          type: string
          description: End Date
          example: ""
        specialOfferIndicator:
          type: string
          description: Special Offer Indicator
          example: "#Aspen-indicator"
        otc:
          type: string
          description: Offer Tracking Code
          example: "#offer tracking code which is POA for sourceCode"
        offerRankOrder:
          type: string
          description: Offer Rank Order
          example: "#Prequal Response"
        treatmentId:
          type: string
          description: Treatment ID
          example: "#Prequal will use this info"
        requestTs:
          type: string
          description: Request Timestamp
          example: ""
        dcfScore:
          type: string
          description: DCF Score
          example: "0.0"
        dcfRevenueScore:
          type: string
          description: DCF Revenue Score
          example: "0.45521"
        controlGrpInd:
          type: string
          description: Control Group Indicator
          example: "3"

    OffersByClient:
      type: object
      properties:
        offers:
          type: array
          items:
            $ref: '#/components/schemas/Offer'

    OfferResponse:
      type: object
      properties:
        global_response:
          $ref: '#/components/schemas/GlobalResponse'
        visitor_identity:
          $ref: '#/components/schemas/VisitorIdentity'
        ASPEN:
          $ref: '#/components/schemas/OffersByClient'
        DM:
          $ref: '#/components/schemas/OffersByClient'

    ErrorResponse:
      type: object
      properties:
        error:
          type: string
          description: Error message
          example: "Invalid input"
