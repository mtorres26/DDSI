const controller = {}
const title = 'INDEX DESDE EL SERVIDOR CON PUG Y DESDE UNA VARIABLE'
controller.index = (req,res)=>{
    res.render('index',{title})
}

module.exports = controller

