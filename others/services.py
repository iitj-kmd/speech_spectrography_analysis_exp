openapi: 3.0.0
info:
  title: Offer Request API
  version: 1.0.0
  description: API for submitting offer requests and retrieving associated product details.
servers:
  - url: https://api.example.com/v1 # Replace with your actual API base URL
    description: Main API server
paths:
  /offerRequest: # Added leading slash to the path
    post:
      summary: Submit an Offer Request
      description: Sends visitor and request details to retrieve applicable offers and product information.
      operationId: submitOfferRequest # Unique identifier for the operation
      tags:
        - Offers
      requestBody:
        description: Details needed to process the offer request. (Schema needs definition based on actual request requirements)
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                visitorIdentifier:
                  type: string
                  description: Unique identifier for the visitor (e.g., hhold, pnr, or custXrefId).
                  example: "N72222054283574082884435368852113564598/9"
                requestContext:
                  type: object
                  description: Additional context for the request (example placeholder).
                  properties:
                    source:
                      type: string
                      example: "WebApp"
              required:
                - visitorIdentifier
      responses:
        '200':
          description: Successful retrieval of offer details.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OfferResponse' # Reference the main response schema below
              example: # The example you provided
                global_response:
                  request_identifier: "OMIASPEN OMI"
                  explanation_message: "Success/Failure"
                  responseTimestamp: "2025-04-10T17:19:54.076-0700"
                visitor_details:
                  hhold: "acc9f96a8a2391460eae12e3704a467f408899476aea85d5185bdd613647678d"
                  pnr: "N72222054283574082884435368852113564598/9"
                  psn: "123456789"
                  custXrefId: "987654321"
                  lastUpdatedTimestamp: "2025-03-09T19:43:00.8365376"
                omi_product_response:
                  aspen:
                    products:
                      - product_metadata:
                          requestId: "S03YF2VhWU7Zh4w3UoNCYMTtr4uvicGH1741401173736"
                          dcfScore: "0.0"
                          dcfRevenueScore": "0.45521"
                          controlGrpInd: "3"
                          decisionStatusCode: null
                          decisionReason: null
                          decisionGroupCode: null
                          pcn: null
                          productEventTimestamp: "2025-03-05T17:19:54.076-0700"
                        product:
                          - iaCode: "RJF"
                            sourceCode: "44601"
                            order: "1"
                            specialOfferIndicator: "Y"
                            startDate: ""
                            endDate: ""
                            eligibility_status: null
                          - iaCode: "BDY"
                            sourceCode: "61482"
                            otc: ""
                            order: "1"
                            specialOfferIndicator": "Y"
                            offer: "94"
                            startDate: ""
                            endDate: ""
                            eligibility_status": null
                      - product_metadata:
                          requestId: "a02RF2VhWU7Zh4w3UoNCYMTtr4uvicGH1841501173712"
                          dcfScore": "0.0"
                          dcfRevenueScore": "0.45521"
                          controlGrpInd: "3"
                          decisionStatusCode": null
                          decisionReason": null
                          decisionGroupCode": null
                          pcn": null
                          productEventTimestamp": "2025-03-06T17:19:54.076-0700"
                        product:
                          - iaCode: "RJF"
                            sourceCode: "44601"
                            order: "1"
                            specialOfferIndicator": "Y"
                            startDate: ""
                            endDate: ""
                            eligibility_status": null
        '400':
          description: Bad Request - Invalid input provided.
        '500':
          description: Internal Server Error - Processing failed.

components:
  schemas:
    OfferResponse:
      type: object
      properties:
        global_response:
          $ref: '#/components/schemas/GlobalResponse'
        visitor_details:
          $ref: '#/components/schemas/VisitorDetails'
        omi_product_response:
          $ref: '#/components/schemas/OmiProductResponse'
    GlobalResponse:
      type: object
      properties:
        request_identifier:
          type: string
          example: "OMIASPEN OMI"
        explanation_message:
          type: string
          example: "Success/Failure"
        responseTimestamp:
          type: string
          format: date-time # ISO 8601 format
          example: "2025-04-10T17:19:54.076-0700"
    VisitorDetails:
      type: object
      properties:
        hhold:
          type: string
          example: "acc9f96a8a2391460eae12e3704a467f408899476aea85d5185bdd613647678d"
        pnr:
          type: string
          example: "N72222054283574082884435368852113564598/9"
        psn:
          type: string
          example: "123456789"
        custXrefId:
          type: string
          example: "987654321"
        lastUpdatedTimestamp:
          type: string
          # format: date-time # Format seems slightly different, keeping as string
          example: "2025-03-09T19:43:00.8365376"
    OmiProductResponse:
      type: object
      properties:
        aspen:
          $ref: '#/components/schemas/AspenResponse'
    AspenResponse:
      type: object
      properties:
        products:
          type: array
          items:
            $ref: '#/components/schemas/ProductEntry'
    ProductEntry:
      type: object
      properties:
        product_metadata:
          $ref: '#/components/schemas/ProductMetadata'
        product:
          type: array
          items:
            $ref: '#/components/schemas/ProductDetail'
    ProductMetadata:
      type: object
      properties:
        requestId:
          type: string
          example: "S03YF2VhWU7Zh4w3UoNCYMTtr4uvicGH1741401173736"
        dcfScore:
          type: string # Assuming string based on example "0.0"
          example: "0.0"
        dcfRevenueScore:
          type: string # Assuming string based on example "0.45521"
          example: "0.45521"
        controlGrpInd:
          type: string # Assuming string based on example "3"
          example: "3"
        decisionStatusCode:
          type: object # Can be any type or null
          nullable: true
          example: null
        decisionReason:
          type: object # Can be any type or null
          nullable: true
          example: null
        decisionGroupCode:
          type: object # Can be any type or null
          nullable: true
          example: null
        pcn:
          type: object # Can be any type or null
          nullable: true
          example: null
        productEventTimestamp:
          type: string
          format: date-time
          example: "2025-03-05T17:19:54.076-0700"
    ProductDetail:
      type: object
      properties:
        iaCode:
          type: string
          example: "RJF"
        sourceCode:
          type: string
          example: "44601"
        otc:
          type: string
          nullable: true
          example: ""
        order:
          type: string # Assuming string based on example "1"
          example: "1"
        specialOfferIndicator:
          type: string
          example: "Y"
        offer:
          type: string
          nullable: true # Example shows it missing sometimes
          example: "94"
        startDate:
          type: string
          # format: date # Could be date if populated
          example: ""
        endDate:
          type: string
          # format: date # Could be date if populated
          example: ""
        eligibility_status:
          type: object # Can be any type or null
          nullable: true
          example: null
