
export default function setRem():void{
  console.log('resizing')
  const html:HTMLElement = document.documentElement
  if(html){
    const rem = html.offsetWidth / 100
    Object.assign(html.style, {
      fontSize:rem + 'px'
    })

    if(html.offsetWidth < 1440){
      document.body.style.overflowX = 'scroll'
    }
  }
}