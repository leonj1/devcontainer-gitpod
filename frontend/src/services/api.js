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
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.text();
  }
}

export const apiStrategy = new DevcontainerApiStrategy();