const webpack = require('webpack');

module.exports = {
  devtool: 'cheap-module-source-map',
  entry: './modules/main.js',
  output: {
    filename: './js/bundle.js'
  },
  plugins: [
 new webpack.DefinePlugin({
  'process.env': {
    'NODE_ENV': JSON.stringify('production')
  }
 }),
 new webpack.optimize.UglifyJsPlugin({
         sourcemap: true,
             beautify: false,
             comments: false,
             compress: {
               warnings: false,
               drop_console: true,
               screw_ie8: true
             },
             mangle: {
               except: [
                 '$', 'webpackJsonp'
               ],
               screw_ie8: true,
               keep_fnames: true
             },
             output: {
               comments: false,
               screw_ie8: true
             }
})
 ],
  module: {

    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        }
      },
      { test: /\.less$/, loader: 'style-loader!css-loader!less-loader' }, // use ! to chain loaders
      { test: /\.css$/, loader: 'style-loader!css-loader' },
      { test: /\.(png|jpg)$/, loader: 'url-loader?limit=8192' } // inline base64 URLs for <=8k images, direct URLs for the rest
    ]
  }
};
