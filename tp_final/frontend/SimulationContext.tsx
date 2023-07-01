import { ReactNode, createContext, useContext, useState } from 'react';

type Props = {
    children: ReactNode;
};

type SimulationContextType = {
  simulationData: Anio[] | null;
  setSimulationData: (data: Anio[] | null) => void;
};

const SimulationContext = createContext<SimulationContextType | undefined>(undefined);

export const SimulationProvider = ({ children }: Props) => {
  const [simulationData, setSimulationData] = useState<Anio[] | null>(null);

  return (
    <SimulationContext.Provider value={{ simulationData, setSimulationData }}>
      {children}
    </SimulationContext.Provider>
  );
};

export const useSimulation = (): SimulationContextType => {
  const context = useContext(SimulationContext);
  if (!context) {
    throw new Error('useSimulation debe ser utilizado dentro de un SimulationProvider');
  }
  return context;
};