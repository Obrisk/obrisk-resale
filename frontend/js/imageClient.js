

/* istanbul ignore next */
function imgClient (OSS) {
    /* istanbul ignore next */
    function objectRequestParams(method, name, options) {
      options = options || {};
      name = this._objectName(name);
      const authResource = `/${this.options.bucket}/${name}`;
      const params = {
        name,
        method,
        host: this.options.imageHost,
        resource: `/${name}`,
        timeout: options.timeout,
        authResource,
        ctx: options.ctx
      };
  
      if (options.headers) {
        params.headers = options.headers;
      }
      return params;
    }
  
    function ImageClient(options) {
      if (!(this instanceof ImageClient)) {
        return new ImageClient(options);
      }
      if (!options.bucket) {
        throw new Error('require bucket for image service instance');
      }
      if (!options.imageHost) {
        throw new Error('require imageHost for image service instance');
      }
  
      this.client = new OSS(options);
      this.client.options.imageHost = options.imageHost;
      this.client._objectRequestParams = objectRequestParams;
    }
  
    /**
     * Image operations
     */
  
    ImageClient.prototype.get = async function get(name, file, options) {
      return await this.client.get(name, file, options);
    };
  
    ImageClient.prototype.getStream = async function getStream(name, options) {
      return await this.client.getStream(name, options);
    };
  
    ImageClient.prototype.getExif = async function getExif(name, options) {
      const params = this.client._objectRequestParams('GET', `${name}@exif`, options);
      params.successStatuses = [200];
  
      let result = await this.client.request(params);
      result = await this._parseResponse(result);
      return {
        res: result.res,
        data: result.data
      };
    };
  
    ImageClient.prototype.getInfo = async function getInfo(name, options) {
      const params = this.client._objectRequestParams('GET', `${name}@infoexif`, options);
      params.successStatuses = [200];
  
      let result = await this.client.request(params);
      result = await this._parseResponse(result);
      return {
        res: result.res,
        data: result.data
      };
    };
  
    ImageClient.prototype.signatureUrl = function signatureUrl(name) {
      return this.client.signatureUrl(name, this.client.options.imageHost);
    };
  
    ImageClient.prototype._parseResponse = async function _parseResponse(result) {
      const str = result.data.toString();
      const type = result.res.headers['content-type'];
  
      if (type === 'application/json') {
        const data = JSON.parse(str);
        result.data = {};
        if (data) {
          Object.keys(data).forEach((key) => {
            result.data[key] = parseFloat(data[key].value, 10) || data[key].value;
          });
        }
      } else if (type === 'application/xml') {
        result.data = await this.client.parseXML(str);
      }
      return result;
    };
  
    return ImageClient;
  };