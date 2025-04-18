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
                $ref: '#/components/schemas/enquiry_response'
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
      example:
        requestID: "OMIASPEN OMI"
    enquiry_response:
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
        explanation_message:
          type: string
          description: Explanation of the response status.
        responseTimestamp:
          type: string
          format: date-time
          description: Timestamp of the response.
    visitor_details:
      type: object
      properties:
        hhold:
          type: string
          description: Household identifier.
        pnr:
          type: string
          description: Passenger Name Record.
        psn:
          type: string
          description: Passenger Service Number.
        custXrefId:
          type: string
          description: Customer cross-reference ID.
        lastUpdatedTimestamp:
          type: string
          format: date-time
          description: Timestamp of the last update.
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
        dcfScore:
          type: string
          description: DCF score.
        dcfRevenueScore:
          type: string
          description: DCF revenue score.
        controlGrpInd:
          type: string
          description: Control group indicator.
        decisionStatusCode:
          type: string
          nullable: true
          description: Decision status code.
        decisionReason:
          type: string
          nullable: true
          description: Decision reason.
        decisionGroupCode:
          type: string
          nullable: true
          description: Decision group code.
        pcn:
          type: string
          nullable: true
          description: PCN.
        productEventTimestamp:
          type: string
          format: date-time
          description: Timestamp of the product event.
    product:
      type: object
      properties:
        iaCode:
          type: string
          description: IA code.
        sourceCode:
          type: string
          description: Source code.
        order:
          type: string
          description: Order.
        specialOfferIndicator:
          type: string
          description: Special offer indicator.
        startDate:
          type: string
          description: Start date.
        endDate:
          type: string
          description: End date.
        eligibility_status:
          type: string
          nullable: true
          description: Eligibility status.
    error_response:
      type: object
      properties:
        error:
          type: string
          description: Error message.
      example:
        error: "Invalid request body"

