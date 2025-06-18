import * as sdk from "@hasura/ndc-lambda-sdk";

/* =============================================== Custom Logic Examples =============================================== */

/**
 * @readonly 
 * Get a new UUID
 * NDC Function: This has the readonly tag, this function will be exposed as a GraphQL query
 */
export function uuid(): string {
  // UUID v4 using crypto.getRandomValues (RFC4122 compliant)
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (char) => {
    const rand = crypto.getRandomValues(new Uint8Array(1))[0] % 16;
    const value = char === 'x' ? rand : (rand & 0x3) | 0x8;
    return value.toString(16);
  });
}

/**
 * Encode a given string in base 64
 * NDC Procedure: As this is missing the readonly tag, this function will be exposed as a mutation in the API)
 */
export function encode(username: string): string {
  return Buffer.from(username).toString("base64");
}


/** ===============================================  Extending a model =============================================== */
/**
 * @readonly
 * Convert all of the given text to upper case
 */
export function capitalise(text: string): string {
  return text.toUpperCase();
}

/* ===============================================  Error Handling=============================================== */
//import * as sdk from "@hasura/ndc-lambda-sdk";

/** 
 * @readonly 
 * Update a resource
 */
export function updateResource(userRole: string): boolean {
  if (userRole !== "admin") {
    throw new sdk.Forbidden("User does not have permission to update this resource", { role: userRole });
  }
  console.log("Resource updated successfully.");
  return true;
}

/** 
 * @readonly 
 * Create a resource
 */
export function createResource(id: string, existingIds: string[]): boolean {
  if (existingIds.includes(id)) {
    throw new sdk.Conflict("Resource with this ID already exists", { existingId: id });
  }
  console.log("Resource created successfully.");
  return true;
}

/** 
 * @readonly 
 * Divide two numbers
 */
export function divide(x: number, y: number): number {
  if (y === 0) {
    throw new sdk.UnprocessableContent("Cannot divide by zero", { myErrorMetadata: "stuff", x, y });
  }
  return x / y;
}

/** ===============================================  HTTP Header Forwarding =============================================== */
//import * as sdk from "@hasura/ndc-lambda-sdk";

/** 
 * @readonly 
 * Forward http headers
 */
export function forwardedHeader(headers: sdk.JSONValue, name: string): string {
  const headersMap = headers.value as Record<string, string>;
  const value = headersMap[name] || "Not Found";
  return `${name} = ${value}`;
}

/* ===============================================  returning HTTP Headers =============================================== */

type HeadersResponse<T> = {
  headers: sdk.JSONValue
  response: T
}

/** 
 * @readonly 
 * Return headers in http response
 */
export function returnHeader(headers: sdk.JSONValue): HeadersResponse<string> {
  const headersMap = headers.value as Record<string, string>;
  headersMap["x-response-header-1"] = "header-1 value set in the code";
  headersMap["x-response-header-2"] = "header-2 value set in the code";
  const headersValue = new sdk.JSONValue(headersMap);
  const responseValue = JSON.stringify(headersMap);
  return {
    headers: headersValue,
    response: responseValue
  };
}