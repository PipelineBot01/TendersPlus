const { override, addWebpackAlias, addLessLoader } = require('customize-cra')

const path = require('path')
module.exports = {
	webpack: override(
		addWebpackAlias({
			'xxx': path.resolve(__dirname, 'src')
		}),
		addLessLoader({
			lessOptions: {
				javascriptEnabled: true
			}
		}),


	)
}