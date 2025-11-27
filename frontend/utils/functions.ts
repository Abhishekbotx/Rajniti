import { ELECTION_TYPES } from "./constants"

const getElectionName = (electionType: string) => {
    return ELECTION_TYPES[electionType as keyof typeof ELECTION_TYPES]
}

export { getElectionName }
