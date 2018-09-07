const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssEsctracPlugin = require('mini-css-extract-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')

module.exports = {
    //entry:{},
    //output:{},
    module:{
        rules:[
            {
                test:/\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader'
                }
            },
            {
                test:/\.html$/,
                use: [
                    {
                        loader:'html-loader',
                        options: {minimize: true}
                    }
                ]
            },
            {
                test:/\.(css|scss)$/,
                use: [
                    'style-loader',
                    MiniCssEsctracPlugin.loader,
                    'css-loader?minimize&sourceMap',
                    'resolve-url-loader',
                    'sass-loader?outputStyle=compressed&sourceMap'
                ]
            },
            {
                test: /\.(jpe?g|png|gif|svg|webpg)$/i,
                use: [
                    'file-loader?name=assets/[name].[ext]'
                ]
            },
            {
                test: /\.(ttf|woff2?|mp4)$/i,
                use: 'file-loader?name=assets/[name].[ext]'
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(['dist/**/*.*']),
        new HtmlWebpackPlugin({
            template:'./src/template.html',
            filename:'./index.html' // takes output folder as reference
        }),
        new MiniCssEsctracPlugin({
            filename:'[name].css',
            chunkFilename:'[id].css' // avoid cache
        })
    ]
}