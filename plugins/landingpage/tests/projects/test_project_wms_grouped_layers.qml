<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" minScale="180000" simplifyMaxScale="1" version="3.13.0-Master" simplifyAlgorithm="0" styleCategories="AllStyleCategories" simplifyLocal="1" labelsEnabled="0" hasScaleBasedVisibilityFlag="1" simplifyDrawingHints="1" simplifyDrawingTol="1" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol force_rhr="0" clip_to_extent="1" name="0" type="fill" alpha="1">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="183,72,75,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory maxScaleDenominator="1e+08" lineSizeType="MM" sizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" penWidth="0" backgroundColor="#ffffff" penColor="#000000" width="15" scaleBasedVisibility="0" rotationOffset="270" penAlpha="255" diagramOrientation="Up" direction="1" spacingUnitScale="3x:0,0,0,0,0,0" enabled="0" height="15" opacity="1" spacing="0" labelPlacementMethod="XHeight" showAxis="0" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" backgroundAlpha="255" barWidth="5" spacingUnit="MM" minScaleDenominator="0">
      <fontProperties description="Noto Sans,10,-1,5,50,0,0,0,0,0,Regular" style="Regular"/>
      <attribute field="" color="#000000" label=""/>
      <axisSymbol>
        <symbol force_rhr="0" clip_to_extent="1" name="" type="line" alpha="1">
          <layer locked="0" class="SimpleLine" pass="0" enabled="1">
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" placement="1" showAll="1" linePlacementFlags="18" dist="0" priority="0" obstacle="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option value="0" name="allowedGapsBuffer" type="double"/>
        <Option value="false" name="allowedGapsEnabled" type="bool"/>
        <Option value="" name="allowedGapsLayer" type="QString"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <referencedLayers/>
  <referencingLayers/>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="gid">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="datum">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bearbeiter">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="veranstaltung">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="beschriftung">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="flaechentyp">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="farbe">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="schraff_width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="schraff_width_prt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="schraff_size">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="schraff_size_prt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="schraff_winkel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="umrissfarbe">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="umrisstyp">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="umrissstaerke">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="umrissstaerke_prt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="umfang">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="flaeche">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bemerkung">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="last_change">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="fid"/>
    <alias name="" index="1" field="gid"/>
    <alias name="" index="2" field="datum"/>
    <alias name="" index="3" field="bearbeiter"/>
    <alias name="" index="4" field="veranstaltung"/>
    <alias name="" index="5" field="beschriftung"/>
    <alias name="" index="6" field="name"/>
    <alias name="" index="7" field="flaechentyp"/>
    <alias name="" index="8" field="farbe"/>
    <alias name="" index="9" field="schraff_width"/>
    <alias name="" index="10" field="schraff_width_prt"/>
    <alias name="" index="11" field="schraff_size"/>
    <alias name="" index="12" field="schraff_size_prt"/>
    <alias name="" index="13" field="schraff_winkel"/>
    <alias name="" index="14" field="umrissfarbe"/>
    <alias name="" index="15" field="umrisstyp"/>
    <alias name="" index="16" field="umrissstaerke"/>
    <alias name="" index="17" field="umrissstaerke_prt"/>
    <alias name="" index="18" field="umfang"/>
    <alias name="" index="19" field="flaeche"/>
    <alias name="" index="20" field="bemerkung"/>
    <alias name="" index="21" field="last_change"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="fid" expression=""/>
    <default applyOnUpdate="0" field="gid" expression=""/>
    <default applyOnUpdate="0" field="datum" expression=""/>
    <default applyOnUpdate="0" field="bearbeiter" expression=""/>
    <default applyOnUpdate="0" field="veranstaltung" expression=""/>
    <default applyOnUpdate="0" field="beschriftung" expression=""/>
    <default applyOnUpdate="0" field="name" expression=""/>
    <default applyOnUpdate="0" field="flaechentyp" expression=""/>
    <default applyOnUpdate="0" field="farbe" expression=""/>
    <default applyOnUpdate="0" field="schraff_width" expression=""/>
    <default applyOnUpdate="0" field="schraff_width_prt" expression=""/>
    <default applyOnUpdate="0" field="schraff_size" expression=""/>
    <default applyOnUpdate="0" field="schraff_size_prt" expression=""/>
    <default applyOnUpdate="0" field="schraff_winkel" expression=""/>
    <default applyOnUpdate="0" field="umrissfarbe" expression=""/>
    <default applyOnUpdate="0" field="umrisstyp" expression=""/>
    <default applyOnUpdate="0" field="umrissstaerke" expression=""/>
    <default applyOnUpdate="0" field="umrissstaerke_prt" expression=""/>
    <default applyOnUpdate="0" field="umfang" expression=""/>
    <default applyOnUpdate="0" field="flaeche" expression=""/>
    <default applyOnUpdate="0" field="bemerkung" expression=""/>
    <default applyOnUpdate="0" field="last_change" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" field="fid" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" constraints="0" field="gid" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="datum" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="bearbeiter" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="veranstaltung" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="beschriftung" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="name" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="flaechentyp" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="farbe" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="schraff_width" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="schraff_width_prt" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="schraff_size" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="schraff_size_prt" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="schraff_winkel" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="umrissfarbe" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="umrisstyp" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="umrissstaerke" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="umrissstaerke_prt" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="umfang" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="flaeche" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="bemerkung" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="last_change" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="gid" desc=""/>
    <constraint exp="" field="datum" desc=""/>
    <constraint exp="" field="bearbeiter" desc=""/>
    <constraint exp="" field="veranstaltung" desc=""/>
    <constraint exp="" field="beschriftung" desc=""/>
    <constraint exp="" field="name" desc=""/>
    <constraint exp="" field="flaechentyp" desc=""/>
    <constraint exp="" field="farbe" desc=""/>
    <constraint exp="" field="schraff_width" desc=""/>
    <constraint exp="" field="schraff_width_prt" desc=""/>
    <constraint exp="" field="schraff_size" desc=""/>
    <constraint exp="" field="schraff_size_prt" desc=""/>
    <constraint exp="" field="schraff_winkel" desc=""/>
    <constraint exp="" field="umrissfarbe" desc=""/>
    <constraint exp="" field="umrisstyp" desc=""/>
    <constraint exp="" field="umrissstaerke" desc=""/>
    <constraint exp="" field="umrissstaerke_prt" desc=""/>
    <constraint exp="" field="umfang" desc=""/>
    <constraint exp="" field="flaeche" desc=""/>
    <constraint exp="" field="bemerkung" desc=""/>
    <constraint exp="" field="last_change" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column name="fid" width="-1" type="field" hidden="0"/>
      <column name="gid" width="-1" type="field" hidden="0"/>
      <column name="datum" width="-1" type="field" hidden="0"/>
      <column name="bearbeiter" width="-1" type="field" hidden="0"/>
      <column name="veranstaltung" width="-1" type="field" hidden="0"/>
      <column name="beschriftung" width="-1" type="field" hidden="0"/>
      <column name="name" width="-1" type="field" hidden="0"/>
      <column name="flaechentyp" width="-1" type="field" hidden="0"/>
      <column name="farbe" width="-1" type="field" hidden="0"/>
      <column name="schraff_width" width="-1" type="field" hidden="0"/>
      <column name="schraff_width_prt" width="-1" type="field" hidden="0"/>
      <column name="schraff_size" width="-1" type="field" hidden="0"/>
      <column name="schraff_size_prt" width="-1" type="field" hidden="0"/>
      <column name="schraff_winkel" width="-1" type="field" hidden="0"/>
      <column name="umrissfarbe" width="-1" type="field" hidden="0"/>
      <column name="umrisstyp" width="-1" type="field" hidden="0"/>
      <column name="umrissstaerke" width="-1" type="field" hidden="0"/>
      <column name="umrissstaerke_prt" width="-1" type="field" hidden="0"/>
      <column name="umfang" width="-1" type="field" hidden="0"/>
      <column name="flaeche" width="-1" type="field" hidden="0"/>
      <column name="bemerkung" width="-1" type="field" hidden="0"/>
      <column name="last_change" width="-1" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="bearbeiter" editable="1"/>
    <field name="bemerkung" editable="1"/>
    <field name="beschriftung" editable="1"/>
    <field name="datum" editable="1"/>
    <field name="farbe" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="flaeche" editable="1"/>
    <field name="flaechentyp" editable="1"/>
    <field name="gid" editable="1"/>
    <field name="last_change" editable="1"/>
    <field name="name" editable="1"/>
    <field name="schraff_size" editable="1"/>
    <field name="schraff_size_prt" editable="1"/>
    <field name="schraff_width" editable="1"/>
    <field name="schraff_width_prt" editable="1"/>
    <field name="schraff_winkel" editable="1"/>
    <field name="umfang" editable="1"/>
    <field name="umrissfarbe" editable="1"/>
    <field name="umrissstaerke" editable="1"/>
    <field name="umrissstaerke_prt" editable="1"/>
    <field name="umrisstyp" editable="1"/>
    <field name="veranstaltung" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="bearbeiter" labelOnTop="0"/>
    <field name="bemerkung" labelOnTop="0"/>
    <field name="beschriftung" labelOnTop="0"/>
    <field name="datum" labelOnTop="0"/>
    <field name="farbe" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="flaeche" labelOnTop="0"/>
    <field name="flaechentyp" labelOnTop="0"/>
    <field name="gid" labelOnTop="0"/>
    <field name="last_change" labelOnTop="0"/>
    <field name="name" labelOnTop="0"/>
    <field name="schraff_size" labelOnTop="0"/>
    <field name="schraff_size_prt" labelOnTop="0"/>
    <field name="schraff_width" labelOnTop="0"/>
    <field name="schraff_width_prt" labelOnTop="0"/>
    <field name="schraff_winkel" labelOnTop="0"/>
    <field name="umfang" labelOnTop="0"/>
    <field name="umrissfarbe" labelOnTop="0"/>
    <field name="umrissstaerke" labelOnTop="0"/>
    <field name="umrissstaerke_prt" labelOnTop="0"/>
    <field name="umrisstyp" labelOnTop="0"/>
    <field name="veranstaltung" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>fid</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
