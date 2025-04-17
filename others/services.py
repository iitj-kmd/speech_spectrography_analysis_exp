components:
  schemas:
    GlobalResponse:
      type: object
      properties:
        request_identifier:
          type: string
          description: Unique identifier for the request.
          example: "OMIASPEN OMI"
        explanation_message:
          type: string
          description: Status of the response (Success/Failure).
          example: "Success"
        responseTimestamp:
          type: string
          format: date-time
          description: Timestamp of the response.
          example: "2025-04-10T17:19:54.076-0700"
    VisitorDetails:
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
          description: Passenger Sequence Number.
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
    ProductMetadata:
      type: object
      properties:
        requestId:
          type: string
          description: Identifier for the product request.
          example: "S03YF2VhWU7Zh4w3UoNCYMTtr4uvicGH1741401173736"
        dcfScore:
          type: string
          description: Discounted Cash Flow score.
          example: "0.0"
        dcfRevenueScore:
          type: string
          description: Discounted Cash Flow revenue score.
          example: "0.45521"
        controlGrpInd:
          type: string
          description: Control group indicator.
          example: "3"
        decisionStatusCode:
          type: string
          nullable: true
          description: Status code of the decision.
          example: null
        decisionReason:
          type: string
          nullable: true
          description: Reason for the decision.
          example: null
        decisionGroupCode:
          type: string
          nullable: true
          description: Code for the decision group.
          example: null
        pcn:
          type: string
          nullable: true
          description: Product control number.
          example: null
        productEventTimestamp:
          type: string
          format: date-time
          description: Timestamp of the product event.
          example: "2025-03-05T17:19:54.076-0700"
    Product:
      type: object
      properties:
        iaCode:
          type: string
          description: Identifier code for the product.
          example: "RJF"
        sourceCode:
          type: string
          description: Source code of the product.
          example: "44601"
        otc:
          type: string
          description: Over-the-counter information (if applicable).
          example: ""
        order:
          type: string
          description: Order number of the product.
          example: "1"
        specialOfferIndicator:
          type: string
          description: Indicator if it's a special offer (Y/N).
          example: "Y"
        offer:
          type: string
          description: Offer details (if applicable).
          example: "94"
        startDate:
          type: string
          description: Start date of the product/offer.
          example: ""
        endDate:
          type: string
          description: End date of the product/offer.
          example: ""
        eligibility_status:
          type: string
          nullable: true
          description: Eligibility status of the product.
          example: null
    ProductResponse:
      type: object
      properties:
        product_metadata:
          $ref: '#/components/schemas/ProductMetadata'
        product:
          type: array
          items:
            $ref: '#/components/schemas/Product'
    OmiProductResponse:
      type: object
      properties:
        type: object
        additionalProperties:
          type: object
          properties:
            products:
              type: array
              items:
                $ref: '#/components/schemas/ProductResponse'
    Root:
      type: object
      properties:
        global_response:
          $ref: '#/components/schemas/GlobalResponse'
        visitor_details:
          $ref: '#/components/schemas/VisitorDetails'
        omi_product_response:
          $ref: '#/components/schemas/OmiProductResponse'
