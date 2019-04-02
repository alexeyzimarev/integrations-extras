from botocore.stub import Stubber


class PricingClientStubber:
    def __init__(self, client):
        self.client = client
        self.stubber = Stubber(client)

    def activate(self):
        self.stubber.activate()

    def stub_describe_services(self, service_codes):
        expected_params = {'FormatVersion': 'aws_v1'}

        describe_services_response = {
            'Services': map(lambda service_code: {'ServiceCode': service_code}, service_codes)
        }

        self.stubber.add_response('describe_services', describe_services_response, expected_params)

    def stub_get_products(self, rate_data):
        if len(rate_data) == 0:
            self.stubber.add_response('get_products', {'PriceList': []})
            return

        for rate_datum in rate_data:
            service_code = rate_datum['service_code']
            term_code = rate_datum['term_code']
            rate_code = rate_datum['rate_code']
            unit = rate_datum['unit']
            price = rate_datum['price']

            expected_params = {
                'FormatVersion': 'aws_v1',
                'ServiceCode': service_code,
                'Filters': [{'Type': 'TERM_MATCH', 'Field': 'RateCode', 'Value': rate_code}],
                'MaxResults': 1
            }

            get_products_response = {
                'PriceList': [
                    '''
                    {{
                        "terms": {{
                            "OnDemand": {{
                                "{0}": {{
                                    "priceDimensions": {{
                                        "{1}": {{
                                            "rateCode": "{1}",
                                            "unit": "{2}",
                                            "pricePerUnit": {{"USD": "{3}"}}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                    '''.format(term_code, rate_code, unit, price)
                ]
            }

            self.stubber.add_response('get_products', get_products_response, expected_params)
