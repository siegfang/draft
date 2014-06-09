package fy.nlp;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;
import java.util.List;

public class ProcessXML {


    public static String processText(String text) {

        // do some thing with text

        return text;

    }

    /**
     * 通过结点快速遍历XML，修改结点文本，输出XML
     * @param xmlFilePath
     * @param resultFilePath
     */
    public static void transformXML(String xmlFilePath, String resultFilePath) {

        try{
            DocumentBuilderFactory dbf =DocumentBuilderFactory.newInstance();
            DocumentBuilder docBuilder = dbf.newDocumentBuilder();
            Document doc = docBuilder.parse(new File(xmlFilePath));

            Node firstItemNode = doc.getFirstChild().getFirstChild();
//            nodes = doc.getFirstChild().getChildNodes();
//            System.out.println("总共有"+nodes.getLength()+"个item");
            int count = 1;
            for (Node itemNode = firstItemNode; itemNode != null;
                 itemNode = itemNode.getNextSibling()) {

//                System.out.println(itemNode.getTextContent());

                for (Node childNode = itemNode.getFirstChild();
                        childNode != null; childNode = childNode.getNextSibling()) {
                    if (childNode.getNodeType() != Node.ELEMENT_NODE){
                        continue;
                    }
                    if(childNode.getNodeName().equals("text")){
                        childNode.setTextContent(transformTokens(childNode.getTextContent()));
                    }

                    if(childNode.getNodeName().equals("summary")){
                        childNode.setTextContent(transformTokens(childNode.getTextContent()));
                    }

                }
                if (count % 2000 == 0) {
                    System.out.println(count + " nodes complete...");
                }
                count ++;
            }

            System.out.println("Start output XML file");

            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            transformerFactory.setAttribute("indent-number", 2);
            Transformer transformer = transformerFactory.newTransformer();
//            transformer.setOutputProperty(OutputKeys.INDENT, "yes");

            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult(new File(resultFilePath));
            transformer.transform(source, result);
        }catch(Exception e){
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {

        String xmlFilePath = "/Users/fangy/data/cl14-unprocessed/jp/music/unlabeled.review";
        String xmlResultFilePath = "unlabeled.review";
        transformXML(xmlFilePath, xmlResultFilePath);

    }
}
