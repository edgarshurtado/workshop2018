const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssEsctracPlugin = require('mini-css-extract-plugin')

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
                test:/\.css$/,
                use: [
                    MiniCssEsctracPlugin.loader,
                    'css-loader'
                ]
            }
        ]
    },
    plugins: [
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