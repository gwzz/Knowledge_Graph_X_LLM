import FocusGraph from "./components/FocusGraphWrapper";
import dataFile from "@/app/data/data";


export default async function Index() {

    const fgData = JSON.stringify(dataFile)

    return (
        <div>
            <FocusGraph data={fgData}/>
        </div>
    );
}
