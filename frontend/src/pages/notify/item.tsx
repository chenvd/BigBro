import {theme} from "antd";

export function NotifyItem(props: { name: string, icon: string, size?: number }) {
    return (
        <div style={{display: "flex", alignItems: 'center'}}>
            <NotifyItemIcon icon={props.icon} size={props.size || 30}/>
            <span style={{marginLeft: 3}}>{props.name}</span>
        </div>
    )
}

export function NotifyItemIcon(props: { icon: string, size: number }) {

    const {token} = theme.useToken()

    return (
        <img style={{
            height: props.size,
            width: props.size,
            borderColor: token.colorBorder,
            borderWidth: 1,
            borderRadius: props.size / 2,
            borderStyle: 'solid'
        }} src={props.icon} alt=""/>
    )
}
