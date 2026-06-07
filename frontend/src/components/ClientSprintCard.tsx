export function ClientSprintCard({name,status}:{name:string,status:string}){
  return <div style={{border:'1px solid #ddd',borderRadius:16,padding:20}}><h3>{name}</h3><p>{status}</p></div>
}
