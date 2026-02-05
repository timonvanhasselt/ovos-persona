// PersonaResponse.qml
import QtQuick 2.0
import QtQuick.Controls 2.0

Item {
    anchors.fill: parent

    Column {
        spacing: 10
        anchors.centerIn: parent

        Text {
            id: titleText
            text: sessionData.title
            font.pointSize: 24
            font.bold: true
            color: "white"
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: responseText
            text: sessionData.text
            font.pointSize: 18
            color: "lightgray"
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
        }
    }
}
