/**
 * the research fields are derived from 
 * https://www.studyaustralia.gov.au/english/study/universities-higher-education/list-of-australian-universities
 */
import type { ResearchFields } from "../types"

export  const researchFields:ResearchFields = {
  d_01:{
    field:'MATHEMATICAL',
    sub_fields:['Pure Mathematics', 
      'Applied Mathematics', 
      'Numerical and Computational Mathematics', 
      'Statistics',
      'Mathematical Physics',
      'Other Mathematical']
  },
  d_02:{
    field:'PHYSICAL',
    sub_fields:['Astronomical and Space Sciences',
      'Atomic, Molecular, Nuclear, Particle and Plasma Physics', 
      'Classical Physics',
      'Condensed Matter Physics',
      'Optical Physics', 
      'Quantum Physics', 
      'Other Physics']
  },
  d_03:{
    field:'CHEMICAL',
    sub_fields:[]
  },
  d_04:{
    field:'EARTH',
    sub_fields:[]
  },
  d_05:{
    field:'ENVIRONMENTAL',
    sub_fields:[]
  },
  d_06:{
    field:'BIOLOGICAL',
    sub_fields:[]
  },
  d_07:{
    field:'AGRICULTURAL AND VETERINARY',
    sub_fields:[]
  },
  d_08:{
    field:'INFORMATION AND COMPUTINGs',
    sub_fields:[]
  },
  d_09:{
    field:'ENGINEERING',
    sub_fields:[]
  },
  d_10:{
    field:'TECHNOLOGY',
    sub_fields:[]
  },
  d_11:{
    field:'MEDICAL AND HEALTH',
    sub_fields:[]
  },
    	d_12:{
    field:'BUILT ENVIRONMENT AND DESIGN',
    sub_fields:[]
  },
    	d_13:{
    field:'EDUCATION',
    sub_fields:[]
  },
    	d_14:{
    field:'ECONOMICS',
    sub_fields:[]
  },
    	d_15:{
    field:'COMMERCE, MANAGEMENT, TOURISM AND SERVICES',
    sub_fields:[]
  },
    	d_16:{
    field:'STUDIES IN HUMAN SOCIETY',
    sub_fields:[]
  },
    	d_17:{
    field:'PSYCHOLOGY AND COGNITIVE SCIENCES',
    sub_fields:[]
  },
    	d_18:{
    field:'LAW AND LEGAL STUDIES',
    sub_fields:[]
  },
    	d_19:{
    field:'STUDIES IN CREATIVE ARTS AND WRITING',
    sub_fields:[]
  },
    	d_20:{
    field:'LANGUAGE, COMMUNICATION AND CULTURE',
    sub_fields:[]
  },
    	d_21:{
    field:'HISTORY AND ARCHAEOLOGY',
    sub_fields:[]
  },
    	d_22:{
    field:'PHILOSOPHY AND RELIGIOUS STUDIES',
    sub_fields:[]
  }
}
