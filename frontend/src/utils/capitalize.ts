export default function capitalize(s:string):string{
	const temp = s.toLowerCase()
	return temp[0].toUpperCase() + temp.slice(1)
}