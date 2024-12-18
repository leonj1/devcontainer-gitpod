class ApiStrategy {
  async convert(input) {
    throw new Error('Convert method must be implemented');
  }
}

class DevcontainerApiStrategy extends ApiStrategy {
  async convert(input) {
    const response = await fetch('https://devcontainer-api.joseserver.com/convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: input,
    });
    
    if (!response.ok) {
      const errorData = {
        status: response.status,
        message: `Request failed with status ${response.status}`,
        details: null
      };

      try {
        // Try to parse error details from response
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
          errorData.details = await response.json();
          if (errorData.details.detail) {
            errorData.message = Array.isArray(errorData.details.detail) 
              ? errorData.details.detail[0].msg 
              : errorData.details.detail;
          }
        } else {
          errorData.details = await response.text();
        }
      } catch (parseError) {
        console.error('Error parsing error response:', parseError);
      }

      throw errorData;
    }
    
    return response.text();
  }
}

export const apiStrategy = new DevcontainerApiStrategy();
