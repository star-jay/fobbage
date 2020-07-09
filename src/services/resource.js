/**
 * Resource class
 */

class Resource {
  constructor(client, base, otherActions) {
    this.base = base;
    this.client = client;
    Object.assign(this, otherActions);
  }

  get(id, options) {
    let axiosOptions = options;
    let url = `/${this.base}/`;
    // If only an object is passed, those will be options
    if (typeof id === 'object') {
      axiosOptions = id;
    // Anything else will be the id of the resource
    } else if (id !== undefined) {
      url += `${id}/`;
    }
    if (axiosOptions && axiosOptions.nextUrl !== undefined) {
      // next = next page with same options using the cursor
      return this.client.get(axiosOptions.nextUrl);
    }
    return this.client.get(url, axiosOptions);
  }

  delete(id, options) {
    const url = `/${this.base}/${id}/`;
    return this.client.delete(url, options);
  }

  post(options) {
    const url = `/${this.base}/`;
    return this.client.post(url, options);
  }

  put(id, options) {
    const url = `/${this.base}/${id}/`;
    return this.client.put(url, options);
  }

  patch(id, options) {
    const url = `/${this.base}/${id}/`;
    return this.client.patch(url, options);
  }
}

export default Resource;
