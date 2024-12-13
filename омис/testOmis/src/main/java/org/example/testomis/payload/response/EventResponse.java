package org.example.testomis.payload.response;

import lombok.Builder;
import org.example.testomis.model.enums.EventCategory;

@Builder
public record EventResponse (
        int id,

        String name,

        String category,

        String author,

        String start,

        String finish
) {
}
