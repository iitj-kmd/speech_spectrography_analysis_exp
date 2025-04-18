openapi: 3.0.0
info:
  title: Enquiry API
  description: API for handling enquiries
  version: 1.0.0
paths:
  /enquiry:
    post:
      summary: Submit an enquiry
      description: This endpoint allows users to submit enquiries.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/enquiry_request'

      responses:
        '200':
          description: Successful enquiry submission
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/offer_response'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/error_response'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/error_response'
components:
  schemas:
    enquiry_request:
      type: object
      properties:
        requestID:
          type: string
          description: The request identifier string.
          example: "OMIASPEN OMI"
    offer_response:
      type: object
      properties:
        global_response:
          $ref: '#/components/schemas/global_response'
        visitor_details:
          $ref: '#/components/schemas/visitor_details'
        omi_product_response:
          $ref: '#/components/schemas/omi_product_response'
    global_response:
      type: object
      properties:
        request_identifier:
          type: string
          description: The request identifier.
          example: "OMIASPEN OMI"
        explanation_message:
          type: string
          description: Explanation of the response status.
          example: "Success"
        responseTimestamp:
          type: string
          format: date-time
          description: Timestamp of the response.
          example: "2025-04-10T17:19:54.076-0700"
    visitor_details:
      type: object
      properties:
        hhold:
          type: string
          description: Household identifier.
          example: "acc9f96a8a2391460eae12e3704a467f408899476aea85d5185bdd613647678d"
        pnr:
          type: string
          description: Passenger Name Record.
          example: "N72222054283574082884435368852113564598/9"
        psn:
          type: string
          description: Passenger Service Number.
          example: "123456789"
        custXrefId:
          type: string
          description: Customer cross-reference ID.
          example: "987654321"
        lastUpdatedTimestamp:
          type: string
          format: date-time
          description: Timestamp of the last update.
          example: "2025-03-09T19:43:00.8365376"
    omi_product_response:
      type: object
      properties:
        aspen:
          $ref: '#/components/schemas/products_info'
        code:
          $ref: '#/components/schemas/products_info'
    products_info:
      type: object
      properties:
        products:
          type: array
          items:
            $ref: '#/components/schemas/product_info'
    product_info:
      type: object
      properties:
        product_metadata:
          $ref: '#/components/schemas/product_metadata'
        product:
          type: array
          items:
            $ref: '#/components/schemas/product'
    product_metadata:
      type: object
      properties:
        requestId:
          type: string
          description: Request identifier for the product.
          example: "S03YF2VhWU7Zh4w3UoNCYMTtr4uvicGH1741401173736"
        dcfScore:
          type: string
          description: DCF score.
          example: "0.0"
        dcfRevenueScore:
          type: string
          description: DCF revenue score.
          example: "0.45521"
        controlGrpInd:
          type: string
          description: Control group indicator.
          example: "3"
        decisionStatusCode:
          type: string
          nullable: true
          description: Decision status code.
          example: null
        decisionReason:
          type: string
          nullable: true
          description: Decision reason.
          example: null
        decisionGroupCode:
          type: string
          nullable: true
          description: Decision group code.
          example: null
        pcn:
          type: string
          nullable: true
          description: PCN.
          example: null
        productEventTimestamp:
          type: string
          format: date-time
          description: Timestamp of the product event.
          example: "2025-03-05T17:19:54.076-0700"
    product:
      type: object
      properties:
        iaCode:
          type: string
          description: IA code.
          example: "RJF"
        sourceCode:
          type: string
          description: Source code.
          example: "44601"
        order:
          type: string
          description: Order.
          example: "1"
        specialOfferIndicator:
          type: string
          description: Special offer indicator.
          example: "Y"
        startDate:
          type: string
          description: Start date.
          example: ""
        endDate:
          type: string
          description: End date.
          example: ""
        eligibility_status:
          type: string
          nullable: true
          description: Eligibility status.
          example: null
    error_response:
      type: object
      properties:
        error:
          type: string
          description: Error message.
          example: "Invalid request body"

